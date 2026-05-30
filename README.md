# SQL Practice — Local Web App

A fully self-contained SQL practice environment that runs in your browser with a live SQLite backend.

## Quick Start

```bash
cd sql-practice
pip3 install -r requirements.txt
python3 app.py
```

Open **http://localhost:5000** in your browser.

## What's inside

### Practice Questions (53 total)

| Category | # | Topics |
|---|---|---|
| Basic Queries | 10 | SELECT, WHERE, LIKE, BETWEEN, IN, IS NULL, aliases, AND/OR |
| Sorting & Limiting | 3 | ORDER BY, LIMIT, OFFSET, Top-N |
| Aggregates | 3 | COUNT, SUM, AVG, MIN, MAX |
| Distinct & Dedup | 2 | DISTINCT, COUNT DISTINCT |
| Group By & Having | 3 | GROUP BY, HAVING, combined WHERE+HAVING |
| Joins | 5 | INNER, LEFT, SELF, Multi-table, JOIN+Aggregate |
| Subqueries | 4 | Scalar, IN, Correlated, EXISTS |
| Window Functions | 5 | ROW_NUMBER, RANK, DENSE_RANK, LAG/LEAD, Running Total, NTILE |
| CTEs | 2 | Basic CTE, Multi-step CTE |
| Set Operations | 3 | UNION ALL, INTERSECT, EXCEPT |
| String Functions | 2 | UPPER, SUBSTR, LENGTH, INSTR, CASE |
| Date Functions | 2 | STRFTIME, Date Arithmetic |
| NULL Handling | 2 | COALESCE, NULLIF |
| DDL & Indexes | 2 | CREATE TABLE, CREATE/DROP INDEX |
| Advanced | 5 | Conditional Aggregation, Top-N per Group, Revenue Rank, MoM Growth, Recursive CTE |

### Theory Pages (8 topics)

- **ACID Properties** — Atomicity, Consistency, Isolation, Durability
- **Indexing** — B-Tree internals, types, leftmost prefix rule, EXPLAIN
- **Normalization** — 1NF → 2NF → 3NF → BCNF with before/after table examples
- **Triggers** — BEFORE/AFTER, NEW/OLD, audit log and validation examples
- **Views** — Regular vs Materialized, security, updatability
- **Transactions** — BEGIN/COMMIT/ROLLBACK, Savepoints, Isolation Levels, MVCC
- **Joins Visual Guide** — Every JOIN type with ASCII diagrams and example output
- **Window Functions Deep Dive** — OVER, PARTITION BY, frame clauses, all functions

### Sample Database (6 tables)

| Table | Rows | Description |
|---|---|---|
| `employees` | 20 | Name, dept, salary, hire_date, manager, gender |
| `departments` | 6 | Name, location, budget |
| `customers` | 15 | Name, email, city, country, signup_date |
| `products` | 15 | Name, category, price, stock |
| `orders` | 25 | Customer, product, qty, date, status, total |
| `sales` | 25 | Employee, amount, date, region |

## Features

- **Live SQL execution** — queries run against a real SQLite in-memory database
- **Syntax-highlighted editor** — CodeMirror with SQL mode and Dracula theme
- **Keyboard shortcuts** — `Ctrl+Enter` / `Cmd+Enter` to run, `Ctrl+/` to comment
- **Solution panel** — shows the solution query and a step-by-step explanation
- **Table viewer** — browse schema and sample data for any table (modal or full browser)
- **Search** — filter questions by title in the sidebar
- **Safety** — only SELECT/WITH queries are allowed; all DDL/DML is blocked

## File Structure

```
sql-practice/
├── app.py                  Flask app + API routes
├── requirements.txt
├── db/
│   └── seed.py             Creates tables and inserts all sample data
├── content/
│   ├── questions.py        All 53 questions with solutions and explanations
│   └── theory.py           All 8 theory pages
├── static/
│   ├── css/style.css       Dark IDE theme
│   └── js/app.js           SPA logic, CodeMirror, API calls
└── templates/
    └── index.html          Single-page shell
```
