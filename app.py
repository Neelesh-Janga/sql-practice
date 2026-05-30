import re
import sqlite3
import threading

from flask import Flask, jsonify, render_template, request

from content.questions import CATEGORIES, QUESTIONS
from content.theory import THEORY_PAGES
from db.seed import seed_database

app = Flask(__name__)

# ─── In-memory SQLite database ──────────────────────────────────────────────
# check_same_thread=False is safe here because we use a lock for access.
_db_conn = sqlite3.connect(":memory:", check_same_thread=False)
_db_conn.row_factory = sqlite3.Row
_db_lock = threading.Lock()

seed_database(_db_conn)


# ─── Helpers ────────────────────────────────────────────────────────────────
_BLOCKED = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|ATTACH|DETACH|PRAGMA|VACUUM|REINDEX)\b",
    re.IGNORECASE,
)


def _is_safe(sql: str) -> bool:
    """Allow only SELECT statements; reject any DDL / DML."""
    stripped = sql.strip()
    if not stripped.upper().startswith("SELECT") and not stripped.upper().startswith("WITH"):
        return False
    return not bool(_BLOCKED.search(stripped))


def _run_query(sql: str):
    """Execute a SELECT query and return (columns, rows) or raise."""
    with _db_lock:
        cur = _db_conn.execute(sql)
        columns = [d[0] for d in cur.description]
        rows = [list(r) for r in cur.fetchmany(500)]  # cap at 500 rows
    return columns, rows


def _table_info(table: str):
    """Return column info for a table."""
    with _db_lock:
        cur = _db_conn.execute(f"PRAGMA table_info({table})")
        return [dict(r) for r in cur.fetchall()]


def _table_sample(table: str, limit: int = 5):
    """Return sample rows from a table."""
    with _db_lock:
        cur = _db_conn.execute(f"SELECT * FROM {table} LIMIT {limit}")
        columns = [d[0] for d in cur.description]
        rows = [list(r) for r in cur.fetchall()]
    return columns, rows


# ─── Routes ─────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/categories")
def api_categories():
    return jsonify(CATEGORIES)


@app.route("/api/questions")
def api_questions():
    category = request.args.get("category")
    result = []
    for q in QUESTIONS:
        if category is None or q["category"] == category:
            result.append({
                "id": q["id"],
                "category": q["category"],
                "title": q["title"],
                "tables_used": q["tables_used"],
            })
    return jsonify(result)


@app.route("/api/question/<int:qid>")
def api_question(qid: int):
    for q in QUESTIONS:
        if q["id"] == qid:
            return jsonify(q)
    return jsonify({"error": "Question not found"}), 404


@app.route("/api/run", methods=["POST"])
def api_run():
    data = request.get_json(silent=True) or {}
    sql = (data.get("sql") or "").strip()
    if not sql:
        return jsonify({"error": "No SQL provided."}), 400
    if not _is_safe(sql):
        return jsonify({
            "error": "Only SELECT / WITH queries are allowed in this sandbox.\n"
                     "DDL and DML (INSERT, UPDATE, DELETE, DROP, CREATE) are not permitted."
        }), 400
    try:
        columns, rows = _run_query(sql)
        return jsonify({"columns": columns, "rows": rows, "count": len(rows)})
    except sqlite3.Error as exc:
        return jsonify({"error": str(exc)}), 400


@app.route("/api/tables")
def api_tables():
    tables = ["employees", "departments", "customers", "products", "orders", "sales"]
    result = {}
    for t in tables:
        cols, rows = _table_sample(t)
        schema = _table_info(t)
        result[t] = {
            "columns": cols,
            "sample_rows": rows,
            "schema": schema,
        }
    return jsonify(result)


@app.route("/api/theory")
def api_theory():
    return jsonify([
        {"slug": p["slug"], "title": p["title"], "icon": p["icon"], "summary": p["summary"]}
        for p in THEORY_PAGES
    ])


@app.route("/api/theory/<slug>")
def api_theory_detail(slug: str):
    for page in THEORY_PAGES:
        if page["slug"] == slug:
            return jsonify(page)
    return jsonify({"error": "Theory page not found"}), 404


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("RENDER") is None   # debug=False on Render
    if debug:
        print("\n  SQL Practice App is running!")
        print(f"  Open http://localhost:{port} in your browser.\n")
    app.run(host="0.0.0.0", port=port, debug=debug)
