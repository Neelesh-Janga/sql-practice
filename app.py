import os
import re
import sqlite3
import threading

from flask import Flask, jsonify, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from content.questions import CATEGORIES, QUESTIONS
from content.theory import THEORY_PAGES
from db.seed import seed_database

app = Flask(__name__)

# ─── Hard limits ────────────────────────────────────────────────────────────
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024          # 16 KB max request body
app.config["JSON_SORT_KEYS"]     = False

# ─── Rate limiter ────────────────────────────────────────────────────────────
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["300 per hour", "60 per minute"],
    storage_uri="memory://",
    strategy="fixed-window",
)

# ─── In-memory SQLite database ───────────────────────────────────────────────
_db_conn = sqlite3.connect(":memory:", check_same_thread=False)
_db_conn.row_factory = sqlite3.Row
_db_lock = threading.Lock()
seed_database(_db_conn)


# ─── Security headers ────────────────────────────────────────────────────────
@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"]  = "nosniff"
    response.headers["X-Frame-Options"]         = "DENY"
    response.headers["X-XSS-Protection"]        = "1; mode=block"
    response.headers["Referrer-Policy"]         = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"]      = "geolocation=(), microphone=(), camera=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
        "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
        "font-src 'self' data: https://cdnjs.cloudflare.com; "
        "img-src 'self' data:; "
        "connect-src 'self'; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'none';"
    )
    # Prevent browsers from caching API responses
    if request.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-store"
    return response


# ─── Method and path guards ──────────────────────────────────────────────────
_ALLOWED_METHODS = {"GET", "POST", "HEAD", "OPTIONS"}

@app.before_request
def guard_request():
    # Block uncommon HTTP methods (TRACE, PUT, DELETE, PATCH, CONNECT)
    if request.method not in _ALLOWED_METHODS:
        return jsonify({"error": "Method not allowed"}), 405

    # Block any upload-style paths
    path = request.path.lower()
    if any(seg in path for seg in ("/upload", "/file", "/import", "/export", "/exec", "/eval", "/shell")):
        return jsonify({"error": "Not found"}), 404

    # Reject requests with null bytes anywhere
    if b"\x00" in (request.data or b""):
        return jsonify({"error": "Invalid request"}), 400


# ─── Error handlers ──────────────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(_):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Not found"}), 404
    return render_template("index.html"), 404

@app.errorhandler(405)
def method_not_allowed(_):
    return jsonify({"error": "Method not allowed"}), 405

@app.errorhandler(413)
def too_large(_):
    return jsonify({"error": "Request body too large (max 16 KB)"}), 413

@app.errorhandler(429)
def rate_limited(_):
    return jsonify({"error": "Too many requests. Please slow down."}), 429

@app.errorhandler(500)
def server_error(_):
    return jsonify({"error": "Internal server error"}), 500


# ─── SQL sandbox ─────────────────────────────────────────────────────────────
_BLOCKED_KEYWORDS = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|ATTACH|DETACH|PRAGMA|"
    r"VACUUM|REINDEX|LOAD_EXTENSION|REPLACE|UPSERT|TRUNCATE|EXEC|"
    r"EXECUTE|GRANT|REVOKE|COPY|IMPORT|EXPORT)\b",
    re.IGNORECASE,
)

# Patterns that suggest injection attempts even in SELECT context
_SUSPICIOUS = re.compile(
    r"(--|/\*|\*/|xp_|sp_|0x[0-9a-f]+|char\s*\(|concat\s*\(.*\)|"
    r"sleep\s*\(|benchmark\s*\(|waitfor\s+delay|randomblob\s*\(10000)",
    re.IGNORECASE,
)

_MAX_SQL_LEN = 4096   # characters


def _strip_sql_comments(sql: str) -> str:
    """Remove -- and /* */ comments to prevent comment-based bypasses."""
    sql = re.sub(r"--[^\n]*", " ", sql)
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.DOTALL)
    return sql


def _is_safe(sql: str) -> tuple[bool, str]:
    """
    Return (True, "") if query is safe, or (False, reason) otherwise.
    Multi-layer validation:
      1. Length check
      2. Null byte check
      3. Must start with SELECT or WITH
      4. Strip comments, then block DDL/DML keywords
      5. Block multiple statements
      6. Block suspicious injection patterns
    """
    if len(sql) > _MAX_SQL_LEN:
        return False, f"Query too long (max {_MAX_SQL_LEN} characters)."

    if "\x00" in sql:
        return False, "Invalid characters in query."

    upper = sql.lstrip().upper()
    if not (upper.startswith("SELECT") or upper.startswith("WITH")):
        return False, "Only SELECT / WITH queries are allowed."

    clean = _strip_sql_comments(sql)

    if _BLOCKED_KEYWORDS.search(clean):
        return False, "Query contains a disallowed keyword (DDL/DML not permitted)."

    # Multiple statements: semicolons before the final optional one
    if re.search(r";.+", clean.rstrip().rstrip(";")):
        return False, "Multiple SQL statements are not allowed."

    if _SUSPICIOUS.search(clean):
        return False, "Query contains a potentially unsafe pattern."

    return True, ""


def _run_query(sql: str):
    """Execute a sandboxed SELECT and return (columns, rows). Aborts after 500K ops."""
    with _db_lock:
        op_count = [0]

        def _progress():
            op_count[0] += 1
            return 1 if op_count[0] > 500_000 else 0   # 1 = abort

        _db_conn.set_progress_handler(_progress, 50)
        try:
            cur     = _db_conn.execute(sql)
            columns = [d[0] for d in cur.description]
            rows    = [list(r) for r in cur.fetchmany(500)]
        finally:
            _db_conn.set_progress_handler(None, 0)

    return columns, rows


def _table_info(table: str):
    with _db_lock:
        cur = _db_conn.execute(f"PRAGMA table_info({table})")
        return [dict(r) for r in cur.fetchall()]


def _table_sample(table: str, limit: int = 5):
    with _db_lock:
        cur     = _db_conn.execute(f"SELECT * FROM {table} LIMIT {limit}")
        columns = [d[0] for d in cur.description]
        rows    = [list(r) for r in cur.fetchall()]
    return columns, rows


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/categories")
def api_categories():
    return jsonify(CATEGORIES)


@app.route("/api/questions")
def api_questions():
    category = request.args.get("category", "").strip()[:100]  # cap arg length
    result = [
        {"id": q["id"], "category": q["category"],
         "title": q["title"], "tables_used": q["tables_used"]}
        for q in QUESTIONS
        if not category or q["category"] == category
    ]
    return jsonify(result)


@app.route("/api/question/<int:qid>")
def api_question(qid: int):
    if qid < 1 or qid > 10_000:
        return jsonify({"error": "Invalid question ID"}), 400
    for q in QUESTIONS:
        if q["id"] == qid:
            return jsonify(q)
    return jsonify({"error": "Question not found"}), 404


@app.route("/api/run", methods=["POST"])
@limiter.limit("30 per minute")          # tighter limit for query execution
def api_run():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    data = request.get_json(silent=True) or {}
    sql  = (data.get("sql") or "").strip()

    if not sql:
        return jsonify({"error": "No SQL provided."}), 400

    safe, reason = _is_safe(sql)
    if not safe:
        return jsonify({"error": reason}), 400

    try:
        columns, rows = _run_query(sql)
        return jsonify({"columns": columns, "rows": rows, "count": len(rows)})
    except sqlite3.OperationalError as exc:
        msg = str(exc)
        # Scrub internal path info from error messages
        msg = re.sub(r"\b(file|path|directory)\b.*", "[redacted]", msg, flags=re.IGNORECASE)
        return jsonify({"error": msg}), 400
    except sqlite3.Error:
        return jsonify({"error": "Query execution failed."}), 400


@app.route("/api/tables")
def api_tables():
    tables = ["employees", "departments", "customers", "products", "orders", "sales"]
    result = {}
    for t in tables:
        cols, rows = _table_sample(t)
        schema     = _table_info(t)
        result[t]  = {"columns": cols, "sample_rows": rows, "schema": schema}
    return jsonify(result)


@app.route("/api/theory")
def api_theory():
    return jsonify([
        {"slug": p["slug"], "title": p["title"],
         "icon": p["icon"], "summary": p["summary"]}
        for p in THEORY_PAGES
    ])


@app.route("/api/theory/<slug>")
def api_theory_detail(slug: str):
    # Validate slug: only allow alphanumeric and hyphens
    if not re.fullmatch(r"[a-z0-9\-]{1,60}", slug):
        return jsonify({"error": "Invalid slug"}), 400
    for page in THEORY_PAGES:
        if page["slug"] == slug:
            return jsonify(page)
    return jsonify({"error": "Theory page not found"}), 404


if __name__ == "__main__":
    port  = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("RENDER") is None
    if debug:
        print("\n  SQL Practice App is running!")
        print(f"  Open http://localhost:{port} in your browser.\n")
    app.run(host="0.0.0.0", port=port, debug=debug)
