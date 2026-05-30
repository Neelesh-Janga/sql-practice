THEORY_PAGES = [
    {
        "slug": "acid",
        "title": "ACID Properties",
        "icon": "🔒",
        "summary": "The four guarantees that make database transactions reliable.",
        "content": """
<h2>ACID Properties</h2>
<p>ACID is an acronym for the four properties that guarantee reliable database transactions. These properties ensure data integrity even in the presence of errors, failures, or concurrent access.</p>

<h3>A — Atomicity</h3>
<div class="theory-box">
<p><strong>Definition:</strong> A transaction is treated as a single, indivisible unit. Either <em>all</em> operations in the transaction succeed, or <em>none</em> of them do. There is no partial success.</p>

<h4>Real-world example: Bank Transfer</h4>
<pre>BEGIN;
  UPDATE accounts SET balance = balance - 500 WHERE id = 1;  -- debit Alice
  UPDATE accounts SET balance = balance + 500 WHERE id = 2;  -- credit Bob
COMMIT;</pre>

<p>If the system crashes after the debit but before the credit, atomicity ensures the debit is also rolled back. Alice doesn't lose $500 into the void.</p>

<h4>How it's implemented</h4>
<p>Databases use a <strong>Write-Ahead Log (WAL)</strong> or <strong>undo log</strong>. Before modifying data, the original values are written to a log. If a transaction is aborted, the log is replayed in reverse to undo changes.</p>
</div>

<h3>C — Consistency</h3>
<div class="theory-box">
<p><strong>Definition:</strong> A transaction brings the database from one valid state to another valid state. All defined rules (constraints, triggers, cascades) must be satisfied.</p>

<h4>Example</h4>
<p>If a column has a <code>CHECK (balance >= 0)</code> constraint, a transaction that would make balance negative is rejected — the database stays in a valid state.</p>

<pre>-- This will be rejected if balance would go negative:
UPDATE accounts SET balance = balance - 10000 WHERE id = 1;
-- ERROR: CHECK constraint failed: balance >= 0</pre>

<p>Consistency is partly the database's responsibility (enforcing constraints) and partly the application's responsibility (writing correct business logic).</p>
</div>

<h3>I — Isolation</h3>
<div class="theory-box">
<p><strong>Definition:</strong> Concurrent transactions execute as if they were run serially (one after another). Intermediate states of a transaction are not visible to other transactions.</p>

<h4>Problems isolation prevents</h4>
<table>
  <tr><th>Problem</th><th>Description</th></tr>
  <tr><td>Dirty Read</td><td>Transaction A reads data written by Transaction B before B commits. If B rolls back, A read invalid data.</td></tr>
  <tr><td>Non-repeatable Read</td><td>Transaction A reads the same row twice and gets different values because Transaction B modified it between the reads.</td></tr>
  <tr><td>Phantom Read</td><td>Transaction A runs the same query twice and gets different rows because Transaction B inserted/deleted rows between the runs.</td></tr>
</table>

<h4>Isolation Levels</h4>
<table>
  <tr><th>Level</th><th>Dirty Read</th><th>Non-repeatable Read</th><th>Phantom Read</th></tr>
  <tr><td>READ UNCOMMITTED</td><td>Possible</td><td>Possible</td><td>Possible</td></tr>
  <tr><td>READ COMMITTED</td><td>Prevented</td><td>Possible</td><td>Possible</td></tr>
  <tr><td>REPEATABLE READ</td><td>Prevented</td><td>Prevented</td><td>Possible</td></tr>
  <tr><td>SERIALIZABLE</td><td>Prevented</td><td>Prevented</td><td>Prevented</td></tr>
</table>
<p>Higher isolation = stronger guarantees but lower concurrency (more locking). Most databases default to READ COMMITTED.</p>
</div>

<h3>D — Durability</h3>
<div class="theory-box">
<p><strong>Definition:</strong> Once a transaction is committed, it persists permanently — even if the system crashes, loses power, or encounters an error immediately afterward.</p>

<h4>How it's implemented</h4>
<p>When you execute <code>COMMIT</code>, the database writes the transaction data to the <strong>Write-Ahead Log (WAL)</strong> on disk before returning success. On recovery after a crash, the database replays committed transactions from the WAL.</p>

<pre>BEGIN;
  INSERT INTO orders VALUES (999, ...);
COMMIT;  -- data is now durable; a crash right here doesn't lose it</pre>

<p>Durability comes at a cost: disk writes (fsync) are slow. High-performance systems sometimes relax durability (e.g., async replication) at the risk of losing recent data on failure.</p>
</div>

<h3>Summary</h3>
<table>
  <tr><th>Property</th><th>Guarantees</th><th>Keyword</th></tr>
  <tr><td>Atomicity</td><td>All-or-nothing execution</td><td>Rollback</td></tr>
  <tr><td>Consistency</td><td>Valid state → valid state</td><td>Constraints</td></tr>
  <tr><td>Isolation</td><td>Transactions don't interfere</td><td>Locks / MVCC</td></tr>
  <tr><td>Durability</td><td>Committed data survives crashes</td><td>WAL / fsync</td></tr>
</table>
"""
    },
    {
        "slug": "indexing",
        "title": "Indexing",
        "icon": "⚡",
        "summary": "How indexes speed up queries, their trade-offs, and how to use them.",
        "content": """
<h2>Database Indexing</h2>
<p>An index is a separate data structure that allows the database to find rows matching a condition much faster than scanning every row in the table (a <em>full table scan</em>).</p>

<h3>The Problem Without an Index</h3>
<div class="theory-box">
<pre>SELECT * FROM employees WHERE department_id = 3;</pre>
<p>Without an index on <code>department_id</code>, the database must read <strong>every row</strong> in the table and check the condition. For 1 million rows, that's 1 million comparisons — O(n).</p>
</div>

<h3>How a B-Tree Index Works</h3>
<div class="theory-box">
<p>Most databases use a <strong>B-Tree (Balanced Tree)</strong> structure for indexes. Think of it like the index at the back of a book:</p>
<pre>
B-Tree on employees.department_id:

           [3]
          /   \\
        [1,2] [4,5,6]
        / \\    / \\
       1   2  4   5,6
       |   |  |    |
      rows rows rows rows
</pre>
<p>The tree is always balanced — every leaf is at the same depth. Finding a value takes O(log n) comparisons instead of O(n). For 1 million rows, that's ~20 comparisons instead of 1,000,000.</p>
</div>

<h3>Types of Indexes</h3>
<div class="theory-box">
<table>
  <tr><th>Type</th><th>Description</th></tr>
  <tr><td>Single-column</td><td>Index on one column: <code>CREATE INDEX ON employees (department_id)</code></td></tr>
  <tr><td>Composite</td><td>Index on multiple columns: <code>CREATE INDEX ON sales (employee_id, sale_date)</code></td></tr>
  <tr><td>Unique</td><td>Enforces uniqueness + speeds lookups: <code>CREATE UNIQUE INDEX ON customers (email)</code></td></tr>
  <tr><td>Partial (PostgreSQL)</td><td>Index only matching rows: <code>CREATE INDEX ON orders (status) WHERE status != 'Delivered'</code></td></tr>
  <tr><td>Covering</td><td>Index includes all columns needed by the query — no table access needed</td></tr>
  <tr><td>Full-Text</td><td>Specialized index for text search (MATCH/AGAINST in MySQL, GIN in PostgreSQL)</td></tr>
</table>
</div>

<h3>Creating and Dropping Indexes</h3>
<div class="theory-box">
<pre>-- Single-column index
CREATE INDEX idx_emp_dept
    ON employees (department_id);

-- Composite index
CREATE INDEX idx_sales_emp_date
    ON sales (employee_id, sale_date);

-- Unique index
CREATE UNIQUE INDEX idx_cust_email
    ON customers (email);

-- Drop an index
DROP INDEX IF EXISTS idx_emp_dept;

-- View all indexes in SQLite
SELECT name, tbl_name, sql
FROM sqlite_master
WHERE type = 'index';</pre>
</div>

<h3>When Queries Use an Index</h3>
<div class="theory-box">
<table>
  <tr><th>Query Pattern</th><th>Index Used?</th></tr>
  <tr><td><code>WHERE indexed_col = value</code></td><td>Yes ✓</td></tr>
  <tr><td><code>WHERE indexed_col > value</code></td><td>Yes ✓</td></tr>
  <tr><td><code>WHERE indexed_col BETWEEN a AND b</code></td><td>Yes ✓</td></tr>
  <tr><td><code>ORDER BY indexed_col</code></td><td>Yes ✓ (avoids sort)</td></tr>
  <tr><td><code>JOIN ON indexed_col</code></td><td>Yes ✓</td></tr>
  <tr><td><code>WHERE UPPER(indexed_col) = 'X'</code></td><td>No ✗ (function on column)</td></tr>
  <tr><td><code>WHERE indexed_col LIKE '%suffix'</code></td><td>No ✗ (leading wildcard)</td></tr>
  <tr><td><code>WHERE indexed_col != value</code></td><td>Usually No ✗</td></tr>
</table>
</div>

<h3>Composite Index — Leftmost Prefix Rule</h3>
<div class="theory-box">
<p>For <code>CREATE INDEX ON sales (employee_id, sale_date)</code>:</p>
<table>
  <tr><th>Query</th><th>Index Used?</th></tr>
  <tr><td><code>WHERE employee_id = 4</code></td><td>Yes ✓</td></tr>
  <tr><td><code>WHERE employee_id = 4 AND sale_date > '2023-06-01'</code></td><td>Yes ✓ (both columns)</td></tr>
  <tr><td><code>WHERE sale_date > '2023-06-01'</code></td><td>No ✗ (first column missing)</td></tr>
</table>
<p>The index can only be used if the query includes the <strong>leftmost column(s)</strong> of the index.</p>
</div>

<h3>Pros and Cons</h3>
<div class="theory-box">
<table>
  <tr><th>Pros</th><th>Cons</th></tr>
  <tr><td>Dramatically faster SELECT queries</td><td>Slows INSERT / UPDATE / DELETE</td></tr>
  <tr><td>Speeds up JOIN operations</td><td>Consumes additional disk space</td></tr>
  <tr><td>Can eliminate sort operations</td><td>Must be maintained on every write</td></tr>
  <tr><td>Unique indexes enforce data integrity</td><td>Index bloat over time with many updates</td></tr>
</table>
<p><strong>Rule of thumb:</strong> Index columns you frequently filter, join, or sort on. Don't over-index write-heavy tables.</p>
</div>

<h3>EXPLAIN QUERY PLAN (SQLite)</h3>
<div class="theory-box">
<p>Use EXPLAIN to see whether the database is using an index:</p>
<pre>EXPLAIN QUERY PLAN
SELECT * FROM employees WHERE department_id = 3;

-- Without index: SCAN TABLE employees  (full scan)
-- With index:    SEARCH TABLE employees USING INDEX idx_emp_dept (department_id=?)</pre>
</div>
"""
    },
    {
        "slug": "normalization",
        "title": "Normalization",
        "icon": "📐",
        "summary": "Organizing tables to reduce redundancy and improve integrity — 1NF through BCNF with examples.",
        "content": """
<h2>Database Normalization</h2>
<p>Normalization is the process of organizing a relational database to <strong>reduce data redundancy</strong> and <strong>improve data integrity</strong> by decomposing tables according to a set of normal forms.</p>

<h3>Why Normalize?</h3>
<div class="theory-box">
<p>Consider this unnormalized table:</p>
<table>
  <tr><th>order_id</th><th>customer_name</th><th>customer_email</th><th>product</th><th>category</th><th>qty</th></tr>
  <tr><td>1</td><td>Alice</td><td>alice@ex.com</td><td>Laptop</td><td>Electronics</td><td>1</td></tr>
  <tr><td>2</td><td>Alice</td><td>alice@ex.com</td><td>Mouse</td><td>Electronics</td><td>2</td></tr>
  <tr><td>3</td><td>Bob</td><td>bob@ex.com</td><td>Desk</td><td>Furniture</td><td>1</td></tr>
</table>
<p>Problems: Alice's email appears twice (redundancy). If Alice changes her email, you must update multiple rows (update anomaly). You can't store a customer with no orders (insertion anomaly).</p>
</div>

<h3>1NF — First Normal Form</h3>
<div class="theory-box">
<p><strong>Rule:</strong> Each column must hold <em>atomic</em> (indivisible) values, and each row must be uniquely identifiable.</p>
<h4>Violation:</h4>
<table>
  <tr><th>id</th><th>name</th><th>phone_numbers</th></tr>
  <tr><td>1</td><td>Alice</td><td>555-1234, 555-5678</td></tr>
</table>
<p><code>phone_numbers</code> contains multiple values — not atomic.</p>
<h4>1NF Fix:</h4>
<table>
  <tr><th>id</th><th>name</th><th>phone_number</th></tr>
  <tr><td>1</td><td>Alice</td><td>555-1234</td></tr>
  <tr><td>1</td><td>Alice</td><td>555-5678</td></tr>
</table>
<p>Or better: create a separate <code>customer_phones</code> table.</p>
</div>

<h3>2NF — Second Normal Form</h3>
<div class="theory-box">
<p><strong>Rule:</strong> Must be in 1NF, AND every non-key column must depend on the <em>entire</em> primary key (no partial dependency). Only relevant when the primary key is composite.</p>
<h4>Violation (composite PK: order_id + product_id):</h4>
<table>
  <tr><th>order_id</th><th>product_id</th><th>product_name</th><th>qty</th></tr>
  <tr><td>1</td><td>10</td><td>Laptop</td><td>1</td></tr>
  <tr><td>2</td><td>10</td><td>Laptop</td><td>3</td></tr>
</table>
<p><code>product_name</code> depends only on <code>product_id</code>, not on the full PK (order_id + product_id) — partial dependency.</p>
<h4>2NF Fix — split into two tables:</h4>
<table>
  <tr><th>order_id</th><th>product_id</th><th>qty</th></tr>
  <tr><td>1</td><td>10</td><td>1</td></tr>
  <tr><td>2</td><td>10</td><td>3</td></tr>
</table>
<table>
  <tr><th>product_id</th><th>product_name</th></tr>
  <tr><td>10</td><td>Laptop</td></tr>
</table>
</div>

<h3>3NF — Third Normal Form</h3>
<div class="theory-box">
<p><strong>Rule:</strong> Must be in 2NF, AND no non-key column should depend on another non-key column (no transitive dependency).</p>
<h4>Violation:</h4>
<table>
  <tr><th>employee_id</th><th>dept_id</th><th>dept_location</th></tr>
  <tr><td>1</td><td>3</td><td>Chicago</td></tr>
  <tr><td>2</td><td>3</td><td>Chicago</td></tr>
</table>
<p><code>dept_location</code> depends on <code>dept_id</code>, not directly on <code>employee_id</code> — transitive dependency.</p>
<h4>3NF Fix:</h4>
<table>
  <tr><th>employee_id</th><th>dept_id</th></tr>
  <tr><td>1</td><td>3</td></tr>
  <tr><td>2</td><td>3</td></tr>
</table>
<table>
  <tr><th>dept_id</th><th>dept_location</th></tr>
  <tr><td>3</td><td>Chicago</td></tr>
</table>
</div>

<h3>BCNF — Boyce-Codd Normal Form</h3>
<div class="theory-box">
<p><strong>Rule:</strong> Must be in 3NF, AND for every functional dependency X → Y, X must be a superkey (a candidate key or superset of one). BCNF is a stricter version of 3NF that handles edge cases with multiple overlapping candidate keys.</p>
<p>BCNF violations are rare in practice. If your tables are in 3NF, they're usually also in BCNF.</p>
</div>

<h3>Denormalization</h3>
<div class="theory-box">
<p>After normalizing, you sometimes <em>intentionally</em> denormalize for performance. Normalization eliminates redundancy but increases the number of JOINs needed. For read-heavy reporting databases (data warehouses), a <strong>star schema</strong> or flat denormalized tables can be faster.</p>
<table>
  <tr><th></th><th>Normalized (OLTP)</th><th>Denormalized (OLAP/DW)</th></tr>
  <tr><td>Redundancy</td><td>Low</td><td>High</td></tr>
  <tr><td>Write speed</td><td>Fast</td><td>Slow</td></tr>
  <tr><td>Read speed</td><td>Slower (many JOINs)</td><td>Faster (fewer JOINs)</td></tr>
  <tr><td>Use case</td><td>Transactional apps</td><td>Analytics / reporting</td></tr>
</table>
</div>
"""
    },
    {
        "slug": "triggers",
        "title": "Triggers",
        "icon": "⚙️",
        "summary": "Automatic actions that fire in response to INSERT, UPDATE, or DELETE events.",
        "content": """
<h2>Triggers</h2>
<p>A trigger is a stored procedure that automatically executes in response to a specific event (INSERT, UPDATE, or DELETE) on a table. Triggers enforce business rules, maintain audit logs, and propagate changes automatically.</p>

<h3>Syntax</h3>
<div class="theory-box">
<pre>CREATE TRIGGER trigger_name
  { BEFORE | AFTER | INSTEAD OF }
  { INSERT | UPDATE | DELETE }
  ON table_name
  [FOR EACH ROW]
BEGIN
  -- trigger body (SQL statements)
END;</pre>
</div>

<h3>BEFORE vs AFTER</h3>
<div class="theory-box">
<table>
  <tr><th></th><th>BEFORE</th><th>AFTER</th></tr>
  <tr><td>When it fires</td><td>Before the row change</td><td>After the row change</td></tr>
  <tr><td>Can abort the change?</td><td>Yes (raise an error)</td><td>No (change already happened)</td></tr>
  <tr><td>Common use</td><td>Validation, data transformation</td><td>Audit logging, cascading changes</td></tr>
</table>
</div>

<h3>NEW and OLD</h3>
<div class="theory-box">
<p>Inside a trigger body, you can access:</p>
<ul>
  <li><code>NEW.column</code> — the new value (available in INSERT and UPDATE)</li>
  <li><code>OLD.column</code> — the old value (available in UPDATE and DELETE)</li>
</ul>
<table>
  <tr><th>Event</th><th>OLD available?</th><th>NEW available?</th></tr>
  <tr><td>INSERT</td><td>No</td><td>Yes (the inserted row)</td></tr>
  <tr><td>UPDATE</td><td>Yes (before)</td><td>Yes (after)</td></tr>
  <tr><td>DELETE</td><td>Yes (the deleted row)</td><td>No</td></tr>
</table>
</div>

<h3>Example 1: Audit Log Trigger</h3>
<div class="theory-box">
<pre>-- First, create an audit log table
CREATE TABLE salary_audit (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    old_salary  REAL,
    new_salary  REAL,
    changed_at  TEXT DEFAULT (DATETIME('now'))
);

-- Trigger fires after every salary update
CREATE TRIGGER trg_salary_audit
    AFTER UPDATE OF salary ON employees
    FOR EACH ROW
    WHEN OLD.salary != NEW.salary
BEGIN
    INSERT INTO salary_audit (employee_id, old_salary, new_salary)
    VALUES (OLD.id, OLD.salary, NEW.salary);
END;</pre>
<p>Now every time an employee's salary changes, the old and new values are recorded in <code>salary_audit</code> automatically.</p>
</div>

<h3>Example 2: Validation Trigger</h3>
<div class="theory-box">
<pre>-- Prevent negative salary updates
CREATE TRIGGER trg_prevent_negative_salary
    BEFORE UPDATE OF salary ON employees
    FOR EACH ROW
    WHEN NEW.salary < 0
BEGIN
    SELECT RAISE(ABORT, 'Salary cannot be negative');
END;</pre>
<p><code>RAISE(ABORT, message)</code> aborts the transaction and returns an error message. This is how BEFORE triggers prevent invalid changes in SQLite.</p>
</div>

<h3>Example 3: Cascading Update</h3>
<div class="theory-box">
<pre>-- When an order status changes to 'Cancelled', restore product stock
CREATE TRIGGER trg_restore_stock_on_cancel
    AFTER UPDATE OF status ON orders
    FOR EACH ROW
    WHEN NEW.status = 'Cancelled' AND OLD.status != 'Cancelled'
BEGIN
    UPDATE products
    SET stock = stock + OLD.quantity
    WHERE id = OLD.product_id;
END;</pre>
</div>

<h3>Dropping and Viewing Triggers</h3>
<div class="theory-box">
<pre>-- Drop a trigger
DROP TRIGGER IF EXISTS trg_salary_audit;

-- List all triggers in SQLite
SELECT name, tbl_name, sql
FROM sqlite_master
WHERE type = 'trigger';</pre>
</div>

<h3>Pros and Cons</h3>
<div class="theory-box">
<table>
  <tr><th>Pros</th><th>Cons</th></tr>
  <tr><td>Enforce business rules at the DB layer</td><td>Hidden logic — hard to debug and discover</td></tr>
  <tr><td>Audit logging without app changes</td><td>Can slow down writes significantly</td></tr>
  <tr><td>Automatic cascading changes</td><td>Trigger chains can cause unexpected effects</td></tr>
  <tr><td>Works regardless of which app writes data</td><td>Not portable across database engines</td></tr>
</table>
<p><strong>Recommendation:</strong> Use triggers sparingly. Prefer application-layer logic for complex business rules. Triggers are excellent for audit logging and simple validation.</p>
</div>
"""
    },
    {
        "slug": "views",
        "title": "Views",
        "icon": "👁️",
        "summary": "Named, reusable SELECT queries that simplify complex logic and control data access.",
        "content": """
<h2>Views</h2>
<p>A view is a named, stored SELECT query. It behaves like a virtual table — you can query it just like a table, but it doesn't store data itself (unless it's a materialized view).</p>

<h3>Creating and Using Views</h3>
<div class="theory-box">
<pre>-- Create a view: employee details with department name
CREATE VIEW v_employee_details AS
SELECT e.id,
       e.name,
       e.salary,
       e.hire_date,
       d.name     AS department,
       d.location
FROM employees e
INNER JOIN departments d ON e.department_id = d.id;

-- Query the view just like a table
SELECT * FROM v_employee_details WHERE salary > 80000;

-- Drop a view
DROP VIEW IF EXISTS v_employee_details;</pre>
</div>

<h3>Why Use Views?</h3>
<div class="theory-box">
<table>
  <tr><th>Benefit</th><th>Description</th></tr>
  <tr><td>Simplicity</td><td>Hide complex JOINs — users query a simple view</td></tr>
  <tr><td>Security</td><td>Expose only certain columns (hide salary, PII)</td></tr>
  <tr><td>Reusability</td><td>DRY — define a query once, reference it everywhere</td></tr>
  <tr><td>Abstraction</td><td>Rename/reorganize data without changing underlying schema</td></tr>
  <tr><td>Backward compatibility</td><td>Keep a view's interface stable while changing underlying tables</td></tr>
</table>
</div>

<h3>Example: Security-Restricted View</h3>
<div class="theory-box">
<pre>-- Public view: no salary, no PII
CREATE VIEW v_employee_public AS
SELECT id, name, department_id, hire_date, gender
FROM employees;

-- Grant access to this view only, not the base table
-- (in a real DB with permissions)</pre>
</div>

<h3>Regular Views vs Materialized Views</h3>
<div class="theory-box">
<table>
  <tr><th></th><th>Regular View</th><th>Materialized View</th></tr>
  <tr><td>Stores data?</td><td>No — re-runs query each time</td><td>Yes — caches the result</td></tr>
  <tr><td>Always up-to-date?</td><td>Yes</td><td>No — must be refreshed</td></tr>
  <tr><td>Read speed</td><td>Depends on underlying query</td><td>Fast (pre-computed)</td></tr>
  <tr><td>Write overhead</td><td>None</td><td>Refresh cost</td></tr>
  <tr><td>SQLite support</td><td>Yes</td><td>No (use a real table instead)</td></tr>
  <tr><td>PostgreSQL support</td><td>Yes</td><td>Yes (REFRESH MATERIALIZED VIEW)</td></tr>
</table>
</div>

<h3>Updatable Views</h3>
<div class="theory-box">
<p>Simple views (no JOINs, no aggregates, no DISTINCT) are often <em>updatable</em> — you can run INSERT/UPDATE/DELETE on the view and it propagates to the base table.</p>
<pre>-- Update through the view (if it's a simple view):
UPDATE v_employee_details SET salary = 90000 WHERE id = 1;
-- This updates employees.salary directly.</pre>
<p>Views with JOINs, aggregates, or DISTINCT are typically read-only. Use <code>INSTEAD OF</code> triggers to make them "updatable".</p>
</div>
"""
    },
    {
        "slug": "transactions",
        "title": "Transactions",
        "icon": "🔄",
        "summary": "Grouping SQL statements into atomic units with BEGIN, COMMIT, and ROLLBACK.",
        "content": """
<h2>Transactions</h2>
<p>A transaction is a sequence of SQL statements that are treated as a single logical unit of work. If any statement fails, the entire group can be rolled back — leaving the database unchanged.</p>

<h3>Basic Transaction Commands</h3>
<div class="theory-box">
<pre>-- Start a transaction
BEGIN;  -- or BEGIN TRANSACTION;

  -- Your SQL statements:
  UPDATE accounts SET balance = balance - 200 WHERE id = 1;
  UPDATE accounts SET balance = balance + 200 WHERE id = 2;

-- Option A: Commit (make changes permanent)
COMMIT;

-- Option B: Rollback (undo all changes since BEGIN)
ROLLBACK;</pre>
</div>

<h3>Auto-Commit Mode</h3>
<div class="theory-box">
<p>By default, most databases run in <strong>auto-commit mode</strong>: every individual statement is automatically wrapped in its own transaction and committed immediately.</p>
<pre>-- In auto-commit mode, each statement is its own transaction:
INSERT INTO orders VALUES (...);  -- auto-committed
UPDATE products SET stock = ...;  -- auto-committed</pre>
<p>To group multiple statements, you must explicitly use <code>BEGIN</code>.</p>
</div>

<h3>Savepoints</h3>
<div class="theory-box">
<p>Savepoints let you create checkpoints within a transaction. You can roll back to a savepoint without rolling back the entire transaction.</p>
<pre>BEGIN;
  INSERT INTO orders VALUES (101, ...);

  SAVEPOINT before_inventory;
    UPDATE products SET stock = stock - 1 WHERE id = 5;
    -- Oops, stock went negative:
  ROLLBACK TO SAVEPOINT before_inventory;
  -- Order insert is still intact; only inventory update was rolled back

  -- Try a different update or handle the error...
COMMIT;  -- commits only the INSERT, not the rolled-back UPDATE</pre>
</div>

<h3>Isolation Levels</h3>
<div class="theory-box">
<p>Isolation levels control how/when one transaction's changes become visible to other concurrent transactions:</p>

<h4>READ UNCOMMITTED (weakest)</h4>
<p>Can read uncommitted changes from other transactions (dirty reads). Fastest but least safe. Rarely used.</p>

<h4>READ COMMITTED (default in PostgreSQL, Oracle)</h4>
<p>Only reads committed data. Prevents dirty reads. A row can change between two reads in the same transaction (non-repeatable reads are possible).</p>

<h4>REPEATABLE READ (default in MySQL InnoDB)</h4>
<p>Once you read a row, subsequent reads in the same transaction see the same value. Prevents dirty and non-repeatable reads. Phantom rows (new rows inserted by another transaction) may still appear.</p>

<h4>SERIALIZABLE (strongest)</h4>
<p>Transactions execute as if they were serial (one after another). Complete isolation. Slowest due to locking/blocking.</p>

<pre>-- Set isolation level in PostgreSQL:
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- SQLite uses a single-writer model, effectively SERIALIZABLE for writes.</pre>
</div>

<h3>Locks</h3>
<div class="theory-box">
<p>Databases use locks to implement isolation:</p>
<table>
  <tr><th>Lock Type</th><th>Description</th></tr>
  <tr><td>Shared (Read) Lock</td><td>Multiple transactions can read simultaneously. Prevents writes.</td></tr>
  <tr><td>Exclusive (Write) Lock</td><td>Only one transaction can write. Blocks all other reads and writes.</td></tr>
  <tr><td>Deadlock</td><td>Two transactions each hold a lock the other needs. DB detects and kills one.</td></tr>
</table>

<h4>MVCC (Multi-Version Concurrency Control)</h4>
<p>Modern databases (PostgreSQL, MySQL InnoDB, SQLite WAL mode) use MVCC instead of heavy locking. Readers don't block writers; writers don't block readers. Each transaction sees a consistent snapshot of the database from when it started.</p>
</div>

<h3>Error Handling Pattern</h3>
<div class="theory-box">
<pre>-- Typical application-level pattern (pseudocode):
try:
    conn.begin()
    execute("UPDATE accounts SET balance = balance - 200 WHERE id = 1")
    execute("UPDATE accounts SET balance = balance + 200 WHERE id = 2")
    conn.commit()
except Exception:
    conn.rollback()
    raise  # re-raise the error</pre>
<p>Always ROLLBACK in the error path. Leaving a transaction open is a common bug that holds locks and blocks other users.</p>
</div>
"""
    },
    {
        "slug": "joins-guide",
        "title": "Joins Visual Guide",
        "icon": "🔗",
        "summary": "Every type of SQL JOIN explained with Venn diagrams and example output.",
        "content": """
<h2>SQL Joins — Complete Visual Guide</h2>
<p>JOINs combine rows from two or more tables based on a related column. Understanding which JOIN type to use is fundamental to SQL.</p>

<p>We'll use these two simple tables for all examples:</p>
<div class="theory-box">
<table>
  <tr><th colspan="2">employees (A)</th><th>&nbsp;</th><th colspan="2">departments (B)</th></tr>
  <tr><th>id</th><th>dept_id</th><th></th><th>id</th><th>name</th></tr>
  <tr><td>1</td><td>1</td><td></td><td>1</td><td>Engineering</td></tr>
  <tr><td>2</td><td>2</td><td></td><td>2</td><td>Marketing</td></tr>
  <tr><td>3</td><td>3</td><td></td><td>4</td><td>Finance</td></tr>
  <tr><td>4</td><td>NULL</td><td></td><td></td><td></td></tr>
</table>
<p>Employee 3 has dept_id=3, but there's no department with id=3. Employee 4 has no department (NULL). Finance (id=4) has no employees.</p>
</div>

<h3>INNER JOIN</h3>
<div class="theory-box">
<pre>SELECT e.id, d.name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.id;</pre>
<p><strong>Result:</strong> Only rows where dept_id matches in BOTH tables.</p>
<table>
  <tr><th>e.id</th><th>d.name</th></tr>
  <tr><td>1</td><td>Engineering</td></tr>
  <tr><td>2</td><td>Marketing</td></tr>
</table>
<p>Employee 3 (unmatched dept 3), Employee 4 (NULL dept), and Finance (no employees) are ALL excluded.</p>
<pre>   A ∩ B  →  only the overlapping center</pre>
</div>

<h3>LEFT JOIN (LEFT OUTER JOIN)</h3>
<div class="theory-box">
<pre>SELECT e.id, d.name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.id;</pre>
<p><strong>Result:</strong> All rows from the LEFT table (employees), NULLs for unmatched right side.</p>
<table>
  <tr><th>e.id</th><th>d.name</th></tr>
  <tr><td>1</td><td>Engineering</td></tr>
  <tr><td>2</td><td>Marketing</td></tr>
  <tr><td>3</td><td>NULL</td></tr>
  <tr><td>4</td><td>NULL</td></tr>
</table>
<p>Finance (id=4) is still excluded — it has no employees in the LEFT table.</p>
<pre>   All of A, matched part of B</pre>
</div>

<h3>RIGHT JOIN (RIGHT OUTER JOIN)</h3>
<div class="theory-box">
<pre>SELECT e.id, d.name
FROM employees e
RIGHT JOIN departments d ON e.dept_id = d.id;</pre>
<p><strong>Result:</strong> All rows from the RIGHT table (departments), NULLs for unmatched left side.</p>
<table>
  <tr><th>e.id</th><th>d.name</th></tr>
  <tr><td>1</td><td>Engineering</td></tr>
  <tr><td>2</td><td>Marketing</td></tr>
  <tr><td>NULL</td><td>Finance</td></tr>
</table>
<p>Employees 3 and 4 are excluded — their departments don't exist in the RIGHT table.</p>
<p>Note: SQLite does not support RIGHT JOIN. Use <code>FROM departments d LEFT JOIN employees e ...</code> instead (swap table order).</p>
<pre>   Matched part of A, all of B</pre>
</div>

<h3>FULL OUTER JOIN</h3>
<div class="theory-box">
<pre>-- PostgreSQL / Standard SQL:
SELECT e.id, d.name
FROM employees e
FULL OUTER JOIN departments d ON e.dept_id = d.id;

-- SQLite workaround (union of left and right):
SELECT e.id, d.name FROM employees e LEFT  JOIN departments d ON e.dept_id = d.id
UNION
SELECT e.id, d.name FROM departments d LEFT JOIN employees  e ON e.dept_id = d.id;</pre>
<p><strong>Result:</strong> All rows from both tables, NULLs where there's no match on either side.</p>
<table>
  <tr><th>e.id</th><th>d.name</th></tr>
  <tr><td>1</td><td>Engineering</td></tr>
  <tr><td>2</td><td>Marketing</td></tr>
  <tr><td>3</td><td>NULL</td></tr>
  <tr><td>4</td><td>NULL</td></tr>
  <tr><td>NULL</td><td>Finance</td></tr>
</table>
<pre>   All of A ∪ All of B</pre>
</div>

<h3>CROSS JOIN (Cartesian Product)</h3>
<div class="theory-box">
<pre>SELECT e.id, d.name
FROM employees e
CROSS JOIN departments d;</pre>
<p><strong>Result:</strong> Every combination of every row from both tables. 4 employees × 3 departments = 12 rows.</p>
<p>Use cases: generate combinations, test data, calendar grids. Rarely used in practice without a WHERE clause to filter the cartesian product.</p>
</div>

<h3>SELF JOIN</h3>
<div class="theory-box">
<pre>SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;</pre>
<p>Join a table to itself using different aliases. Used for hierarchical data (org charts, category trees) and comparing rows within the same table.</p>
</div>

<h3>Quick Reference</h3>
<div class="theory-box">
<table>
  <tr><th>JOIN Type</th><th>Returns</th></tr>
  <tr><td>INNER JOIN</td><td>Rows matching in BOTH tables</td></tr>
  <tr><td>LEFT JOIN</td><td>All left rows + matched right (NULLs for no match)</td></tr>
  <tr><td>RIGHT JOIN</td><td>Matched left + all right rows (NULLs for no match)</td></tr>
  <tr><td>FULL OUTER JOIN</td><td>All rows from both, NULLs where no match</td></tr>
  <tr><td>CROSS JOIN</td><td>Every combination (m × n rows)</td></tr>
  <tr><td>SELF JOIN</td><td>Table joined with itself (using aliases)</td></tr>
</table>
</div>
"""
    },
    {
        "slug": "window-functions",
        "title": "Window Functions Deep Dive",
        "icon": "📊",
        "summary": "OVER, PARTITION BY, frame clauses, and all window functions compared.",
        "content": """
<h2>Window Functions Deep Dive</h2>
<p>Window functions compute a value for each row based on a "window" of related rows — without collapsing those rows into a single output row (unlike GROUP BY).</p>

<h3>Anatomy of a Window Function</h3>
<div class="theory-box">
<pre>function_name(args) OVER (
    [PARTITION BY col1, col2, ...]
    [ORDER BY col3 [ASC|DESC], ...]
    [frame_clause]
)</pre>
<ul>
  <li><code>PARTITION BY</code> — Divides rows into groups; the function resets for each partition. Omit to treat the entire result as one partition.</li>
  <li><code>ORDER BY</code> — Defines the order within the partition. Required for ranking and running totals.</li>
  <li><code>frame_clause</code> — Specifies which rows around the current row are included in the computation.</li>
</ul>
</div>

<h3>Ranking Functions</h3>
<div class="theory-box">
<pre>SELECT name, salary,
    ROW_NUMBER()  OVER (ORDER BY salary DESC) AS row_num,
    RANK()        OVER (ORDER BY salary DESC) AS rnk,
    DENSE_RANK()  OVER (ORDER BY salary DESC) AS dense_rnk
FROM employees;</pre>
<table>
  <tr><th>salary</th><th>ROW_NUMBER</th><th>RANK</th><th>DENSE_RANK</th></tr>
  <tr><td>95000</td><td>1</td><td>1</td><td>1</td></tr>
  <tr><td>93000</td><td>2</td><td>2</td><td>2</td></tr>
  <tr><td>91000</td><td>3</td><td>3</td><td>3</td></tr>
  <tr><td>91000</td><td>4</td><td>3</td><td>3</td></tr>
  <tr><td>89000</td><td>5</td><td>5 ← skip</td><td>4 ← no skip</td></tr>
</table>
</div>

<h3>Value/Navigation Functions</h3>
<div class="theory-box">
<table>
  <tr><th>Function</th><th>Description</th></tr>
  <tr><td>LAG(col, n, default)</td><td>Value from n rows before current (default n=1)</td></tr>
  <tr><td>LEAD(col, n, default)</td><td>Value from n rows after current</td></tr>
  <tr><td>FIRST_VALUE(col)</td><td>First value in the window frame</td></tr>
  <tr><td>LAST_VALUE(col)</td><td>Last value in the window frame (watch out for default frame!)</td></tr>
  <tr><td>NTH_VALUE(col, n)</td><td>Nth value in the window frame</td></tr>
</table>
<pre>SELECT sale_date, amount,
    LAG(amount, 1, 0)  OVER (ORDER BY sale_date) AS prev_sale,
    LEAD(amount, 1, 0) OVER (ORDER BY sale_date) AS next_sale
FROM sales;</pre>
</div>

<h3>Aggregate Window Functions</h3>
<div class="theory-box">
<p>All aggregate functions (SUM, AVG, COUNT, MIN, MAX) can be used as window functions with OVER().</p>
<pre>SELECT name, salary, department_id,
    SUM(salary)   OVER (PARTITION BY department_id) AS dept_total,
    AVG(salary)   OVER (PARTITION BY department_id) AS dept_avg,
    MAX(salary)   OVER (PARTITION BY department_id) AS dept_max,
    COUNT(*)      OVER (PARTITION BY department_id) AS dept_count,
    -- Percentage of department salary
    ROUND(100.0 * salary /
          SUM(salary) OVER (PARTITION BY department_id), 1) AS pct_of_dept
FROM employees;</pre>
</div>

<h3>NTILE</h3>
<div class="theory-box">
<pre>SELECT name, salary,
    NTILE(4)   OVER (ORDER BY salary DESC) AS quartile,
    NTILE(100) OVER (ORDER BY salary DESC) AS percentile
FROM employees;</pre>
<p>Divides the result into n buckets as evenly as possible. Useful for percentiles and bucketing.</p>
</div>

<h3>Frame Clause</h3>
<div class="theory-box">
<pre>-- Running total (rows from start of partition to current row)
SUM(amount) OVER (
    PARTITION BY employee_id
    ORDER BY sale_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)

-- 3-row moving average (current + 1 before + 1 after)
AVG(amount) OVER (
    ORDER BY sale_date
    ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
)

-- Expanding window from start to end of partition
SUM(amount) OVER (
    PARTITION BY employee_id
    ORDER BY sale_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)</pre>

<h4>Frame boundary keywords</h4>
<table>
  <tr><th>Keyword</th><th>Meaning</th></tr>
  <tr><td>UNBOUNDED PRECEDING</td><td>First row of the partition</td></tr>
  <tr><td>n PRECEDING</td><td>n rows before the current row</td></tr>
  <tr><td>CURRENT ROW</td><td>The current row</td></tr>
  <tr><td>n FOLLOWING</td><td>n rows after the current row</td></tr>
  <tr><td>UNBOUNDED FOLLOWING</td><td>Last row of the partition</td></tr>
</table>

<h4>ROWS vs RANGE</h4>
<ul>
  <li><code>ROWS</code> — physical rows (counts by position)</li>
  <li><code>RANGE</code> — logical range (groups rows with equal ORDER BY values together)</li>
</ul>
<p>Use ROWS for running totals to avoid unexpected behavior when ORDER BY has ties.</p>
</div>

<h3>Window Functions vs GROUP BY</h3>
<div class="theory-box">
<table>
  <tr><th></th><th>GROUP BY + Aggregate</th><th>Window Function</th></tr>
  <tr><td>Rows in output</td><td>One per group</td><td>Same number as input</td></tr>
  <tr><td>Access to original row?</td><td>No — collapsed</td><td>Yes</td></tr>
  <tr><td>Can combine with GROUP BY?</td><td>N/A</td><td>Yes</td></tr>
  <tr><td>Use when</td><td>Summarizing data</td><td>Ranking, running totals, comparisons within groups</td></tr>
</table>
</div>
"""
    },
]
