QUESTIONS = [

    # ─────────────────────────────────────────
    # BASIC QUERIES
    # ─────────────────────────────────────────
    {
        "id": 1,
        "category": "Basic Queries",
        "title": "Select All Employees",
        "description": "Retrieve every column and every row from the <code>employees</code> table.",
        "tables_used": ["employees"],
        "starter_sql": "SELECT -- your query here\nFROM employees;",
        "solution_sql": "SELECT *\nFROM employees;",
        "explanation": """
<h3>How it works</h3>
<p><code>SELECT *</code> tells the database to return <strong>all columns</strong>. The <code>FROM employees</code> clause specifies the source table. No <code>WHERE</code> filter means all rows are returned.</p>
<h3>Key concept</h3>
<p>While convenient during exploration, avoid <code>SELECT *</code> in production queries — it pulls unnecessary columns, wastes bandwidth, and breaks if the schema changes.</p>
"""
    },
    {
        "id": 2,
        "category": "Basic Queries",
        "title": "Select Specific Columns",
        "description": "Retrieve only the <code>name</code> and <code>salary</code> of every employee.",
        "tables_used": ["employees"],
        "starter_sql": "SELECT -- list the columns\nFROM employees;",
        "solution_sql": "SELECT name, salary\nFROM employees;",
        "explanation": """
<h3>How it works</h3>
<p>Listing specific columns instead of <code>*</code> is called a <strong>projection</strong>. The database retrieves only those columns from each row, which reduces the data transferred and makes results easier to read.</p>
"""
    },
    {
        "id": 3,
        "category": "Basic Queries",
        "title": "Filter with WHERE",
        "description": "Find all employees who work in department 1 (Engineering).",
        "tables_used": ["employees"],
        "starter_sql": "SELECT name, department_id, salary\nFROM employees\nWHERE -- condition here;",
        "solution_sql": "SELECT name, department_id, salary\nFROM employees\nWHERE department_id = 1;",
        "explanation": """
<h3>How it works</h3>
<p>The <code>WHERE</code> clause filters rows <em>before</em> they are returned. Only rows where the condition evaluates to <code>TRUE</code> are included in the result set.</p>
<h3>Execution order reminder</h3>
<p>Conceptually: <code>FROM</code> → <code>WHERE</code> → <code>SELECT</code>. Even though you write SELECT first, the engine processes FROM and WHERE first.</p>
"""
    },
    {
        "id": 4,
        "category": "Basic Queries",
        "title": "Comparison Operators",
        "description": "List employees whose salary is greater than 80,000.",
        "tables_used": ["employees"],
        "starter_sql": "SELECT name, salary\nFROM employees\nWHERE -- salary condition;",
        "solution_sql": "SELECT name, salary\nFROM employees\nWHERE salary > 80000\nORDER BY salary DESC;",
        "explanation": """
<h3>Comparison operators</h3>
<ul>
  <li><code>=</code> equal to</li>
  <li><code>&lt;&gt;</code> or <code>!=</code> not equal to</li>
  <li><code>&gt;</code> greater than, <code>&lt;</code> less than</li>
  <li><code>&gt;=</code> greater than or equal, <code>&lt;=</code> less than or equal</li>
</ul>
<p>Adding <code>ORDER BY salary DESC</code> sorts the results from highest to lowest salary.</p>
"""
    },
    {
        "id": 5,
        "category": "Basic Queries",
        "title": "BETWEEN Operator",
        "description": "Find all employees hired between 2019-01-01 and 2021-12-31 (inclusive).",
        "tables_used": ["employees"],
        "starter_sql": "SELECT name, hire_date\nFROM employees\nWHERE hire_date -- use BETWEEN;",
        "solution_sql": "SELECT name, hire_date\nFROM employees\nWHERE hire_date BETWEEN '2019-01-01' AND '2021-12-31'\nORDER BY hire_date;",
        "explanation": """
<h3>BETWEEN ... AND ...</h3>
<p><code>BETWEEN a AND b</code> is inclusive on both ends, equivalent to <code>col &gt;= a AND col &lt;= b</code>. It works on numbers, dates, and strings (alphabetical ordering).</p>
<p>SQLite stores dates as text in <code>YYYY-MM-DD</code> format, so lexicographic comparison works correctly here.</p>
"""
    },
    {
        "id": 6,
        "category": "Basic Queries",
        "title": "IN Operator",
        "description": "Get all employees who are in department 1, 3, or 5.",
        "tables_used": ["employees"],
        "starter_sql": "SELECT name, department_id\nFROM employees\nWHERE -- use IN;",
        "solution_sql": "SELECT name, department_id\nFROM employees\nWHERE department_id IN (1, 3, 5)\nORDER BY department_id;",
        "explanation": """
<h3>IN operator</h3>
<p><code>IN (val1, val2, ...)</code> is shorthand for <code>col = val1 OR col = val2 OR ...</code>. It keeps your query concise when matching against a fixed list of values.</p>
<p>You can also use <code>NOT IN</code> to exclude a list of values.</p>
"""
    },
    {
        "id": 7,
        "category": "Basic Queries",
        "title": "LIKE Pattern Matching",
        "description": "Find all employees whose name starts with the letter 'A'.",
        "tables_used": ["employees"],
        "starter_sql": "SELECT name\nFROM employees\nWHERE name -- use LIKE;",
        "solution_sql": "SELECT name\nFROM employees\nWHERE name LIKE 'A%';",
        "explanation": """
<h3>LIKE wildcards</h3>
<ul>
  <li><code>%</code> matches <strong>zero or more</strong> characters: <code>'A%'</code> = starts with A</li>
  <li><code>_</code> matches <strong>exactly one</strong> character: <code>'_ob'</code> = any char then "ob"</li>
</ul>
<p>Example patterns:</p>
<ul>
  <li><code>'%son'</code> — ends with "son"</li>
  <li><code>'%ar%'</code> — contains "ar" anywhere</li>
  <li><code>'C_ro_'</code> — 5-letter name, C, any char, r, o, any char</li>
</ul>
<p>LIKE is case-insensitive in SQLite by default for ASCII characters.</p>
"""
    },
    {
        "id": 8,
        "category": "Basic Queries",
        "title": "IS NULL Check",
        "description": "Find all employees who do not have a manager (i.e., <code>manager_id</code> is NULL).",
        "tables_used": ["employees"],
        "starter_sql": "SELECT name, manager_id\nFROM employees\nWHERE -- check for NULL;",
        "solution_sql": "SELECT name, manager_id\nFROM employees\nWHERE manager_id IS NULL;",
        "explanation": """
<h3>NULL in SQL</h3>
<p>NULL represents an unknown or missing value. It is <strong>not</strong> the same as 0 or an empty string.</p>
<p><strong>Important:</strong> You cannot use <code>= NULL</code> to test for NULL — it always evaluates to NULL (unknown). You must use <code>IS NULL</code> or <code>IS NOT NULL</code>.</p>
<pre>-- WRONG: returns no rows
WHERE manager_id = NULL

-- CORRECT
WHERE manager_id IS NULL</pre>
"""
    },
    {
        "id": 9,
        "category": "Basic Queries",
        "title": "Column Aliases",
        "description": "Select employee names and salaries. Display the salary column as <code>annual_salary</code> and add a computed column <code>monthly_salary</code> (salary divided by 12).",
        "tables_used": ["employees"],
        "starter_sql": "SELECT name,\n       salary AS annual_salary,\n       -- add monthly_salary\nFROM employees;",
        "solution_sql": "SELECT name,\n       salary        AS annual_salary,\n       ROUND(salary / 12.0, 2) AS monthly_salary\nFROM employees\nORDER BY annual_salary DESC;",
        "explanation": """
<h3>AS keyword</h3>
<p><code>AS alias_name</code> renames a column in the result set. Aliases are used to:</p>
<ul>
  <li>Give computed expressions a readable name</li>
  <li>Shorten long column names</li>
  <li>Avoid duplicate column names in JOINs</li>
</ul>
<p><code>ROUND(val, 2)</code> rounds a number to 2 decimal places.</p>
<p>Note: You cannot use a SELECT alias in the same query's WHERE clause — the WHERE is evaluated before SELECT aliases are assigned. Use a subquery or CTE if you need to filter on a computed alias.</p>
"""
    },
    {
        "id": 10,
        "category": "Basic Queries",
        "title": "AND / OR Logic",
        "description": "Find female employees in the Engineering department (department_id = 1) who earn more than 85,000.",
        "tables_used": ["employees"],
        "starter_sql": "SELECT name, gender, department_id, salary\nFROM employees\nWHERE -- combine conditions;",
        "solution_sql": "SELECT name, gender, department_id, salary\nFROM employees\nWHERE gender = 'F'\n  AND department_id = 1\n  AND salary > 85000;",
        "explanation": """
<h3>AND / OR precedence</h3>
<p><code>AND</code> has higher precedence than <code>OR</code>. To avoid ambiguity, always use parentheses when mixing them:</p>
<pre>WHERE (dept = 1 OR dept = 2) AND salary > 70000</pre>
<p>Without parentheses, <code>WHERE dept = 1 OR dept = 2 AND salary > 70000</code> is parsed as <code>WHERE dept = 1 OR (dept = 2 AND salary > 70000)</code> — likely not what you intended.</p>
"""
    },

    # ─────────────────────────────────────────
    # SORTING & LIMITING
    # ─────────────────────────────────────────
    {
        "id": 11,
        "category": "Sorting & Limiting",
        "title": "ORDER BY Multiple Columns",
        "description": "List all employees sorted by department (ascending), then by salary (descending) within each department.",
        "tables_used": ["employees"],
        "starter_sql": "SELECT name, department_id, salary\nFROM employees\nORDER BY -- multiple columns;",
        "solution_sql": "SELECT name, department_id, salary\nFROM employees\nORDER BY department_id ASC, salary DESC;",
        "explanation": """
<h3>Multi-column ORDER BY</h3>
<p>You can list multiple columns in ORDER BY. The database sorts by the first column; ties are broken by the second column, and so on.</p>
<ul>
  <li><code>ASC</code> — ascending (default, A→Z, 1→9)</li>
  <li><code>DESC</code> — descending (Z→A, 9→1)</li>
</ul>
<p>NULLs are sorted last in ascending order in SQLite.</p>
"""
    },
    {
        "id": 12,
        "category": "Sorting & Limiting",
        "title": "LIMIT and OFFSET",
        "description": "Return the 3rd, 4th, and 5th highest-paid employees (simulate pagination).",
        "tables_used": ["employees"],
        "starter_sql": "SELECT name, salary\nFROM employees\nORDER BY salary DESC\nLIMIT -- add LIMIT and OFFSET;",
        "solution_sql": "SELECT name, salary\nFROM employees\nORDER BY salary DESC\nLIMIT 3 OFFSET 2;",
        "explanation": """
<h3>LIMIT and OFFSET</h3>
<p><code>LIMIT n</code> returns at most <em>n</em> rows. <code>OFFSET k</code> skips the first <em>k</em> rows.</p>
<p>Together they enable <strong>pagination</strong>:</p>
<pre>-- Page 1 (rows 1-10)
LIMIT 10 OFFSET 0

-- Page 2 (rows 11-20)
LIMIT 10 OFFSET 10

-- Page 3 (rows 21-30)
LIMIT 10 OFFSET 20</pre>
<p><strong>Important:</strong> Always pair LIMIT/OFFSET with ORDER BY. Without ORDER BY, the database returns rows in undefined order and your pages will be inconsistent.</p>
"""
    },
    {
        "id": 13,
        "category": "Sorting & Limiting",
        "title": "Top N Records",
        "description": "Find the top 5 most expensive products.",
        "tables_used": ["products"],
        "starter_sql": "SELECT name, price\nFROM products\n-- order and limit;",
        "solution_sql": "SELECT name, price\nFROM products\nORDER BY price DESC\nLIMIT 5;",
        "explanation": """
<h3>Top-N pattern</h3>
<p>The <em>Top-N</em> pattern — ORDER BY + LIMIT — is one of the most common SQL patterns. It's useful for leaderboards, recent records, highest/lowest values, etc.</p>
<p>Note that if there are ties at position N, LIMIT arbitrarily cuts them. To handle ties properly, use window functions like <code>RANK()</code> or <code>DENSE_RANK()</code> (see the Window Functions category).</p>
"""
    },

    # ─────────────────────────────────────────
    # AGGREGATES
    # ─────────────────────────────────────────
    {
        "id": 14,
        "category": "Aggregates",
        "title": "COUNT Rows",
        "description": "How many employees are there in total? Also show how many have a manager assigned.",
        "tables_used": ["employees"],
        "starter_sql": "SELECT\n  COUNT(*) AS total_employees,\n  -- count employees with a manager\nFROM employees;",
        "solution_sql": "SELECT\n  COUNT(*)           AS total_employees,\n  COUNT(manager_id)  AS employees_with_manager\nFROM employees;",
        "explanation": """
<h3>COUNT variations</h3>
<ul>
  <li><code>COUNT(*)</code> — counts all rows including those with NULLs</li>
  <li><code>COUNT(column)</code> — counts only non-NULL values in that column</li>
  <li><code>COUNT(DISTINCT column)</code> — counts distinct non-NULL values</li>
</ul>
<p>In our dataset, some employees have <code>manager_id = NULL</code> (they are top-level managers). <code>COUNT(*)</code> includes them, but <code>COUNT(manager_id)</code> does not.</p>
"""
    },
    {
        "id": 15,
        "category": "Aggregates",
        "title": "SUM, AVG, MIN, MAX",
        "description": "Calculate the total salary bill, average salary, minimum salary, and maximum salary across all employees.",
        "tables_used": ["employees"],
        "starter_sql": "SELECT\n  -- aggregate functions here\nFROM employees;",
        "solution_sql": "SELECT\n  SUM(salary)          AS total_salary_bill,\n  ROUND(AVG(salary), 2) AS average_salary,\n  MIN(salary)          AS min_salary,\n  MAX(salary)          AS max_salary\nFROM employees;",
        "explanation": """
<h3>Aggregate functions</h3>
<table>
  <tr><th>Function</th><th>Returns</th><th>Ignores NULLs?</th></tr>
  <tr><td>SUM(col)</td><td>Sum of all values</td><td>Yes</td></tr>
  <tr><td>AVG(col)</td><td>Arithmetic mean</td><td>Yes</td></tr>
  <tr><td>MIN(col)</td><td>Smallest value</td><td>Yes</td></tr>
  <tr><td>MAX(col)</td><td>Largest value</td><td>Yes</td></tr>
  <tr><td>COUNT(col)</td><td>Number of non-NULL rows</td><td>Yes</td></tr>
</table>
<p>All aggregate functions (except COUNT(*)) silently ignore NULLs when computing their result.</p>
"""
    },
    {
        "id": 16,
        "category": "Aggregates",
        "title": "Aggregate per Group",
        "description": "For each department, show the number of employees and the average salary.",
        "tables_used": ["employees"],
        "starter_sql": "SELECT department_id,\n  -- aggregate functions\nFROM employees\nGROUP BY -- group column;",
        "solution_sql": "SELECT department_id,\n  COUNT(*)            AS num_employees,\n  ROUND(AVG(salary), 2) AS avg_salary\nFROM employees\nGROUP BY department_id\nORDER BY department_id;",
        "explanation": """
<h3>GROUP BY</h3>
<p><code>GROUP BY col</code> collapses all rows with the same value in <em>col</em> into a single summary row. Every column in the SELECT list must either:</p>
<ol>
  <li>Appear in the GROUP BY clause, OR</li>
  <li>Be wrapped in an aggregate function</li>
</ol>
<p>This rule is enforced by most databases (SQLite is permissive but you should follow it).</p>
"""
    },

    # ─────────────────────────────────────────
    # DISTINCT & DEDUP
    # ─────────────────────────────────────────
    {
        "id": 17,
        "category": "Distinct & Dedup",
        "title": "DISTINCT Values",
        "description": "List all unique countries that customers come from.",
        "tables_used": ["customers"],
        "starter_sql": "SELECT -- distinct countries\nFROM customers;",
        "solution_sql": "SELECT DISTINCT country\nFROM customers\nORDER BY country;",
        "explanation": """
<h3>DISTINCT</h3>
<p><code>SELECT DISTINCT col</code> removes duplicate rows from the result. It applies to the entire row produced by SELECT, not just one column.</p>
<pre>-- Two distinct columns: eliminates rows where BOTH city AND country are the same
SELECT DISTINCT city, country FROM customers;</pre>
<p>Performance note: DISTINCT often requires a sort or hash operation — it can be slow on large datasets. If you're using it to hide a bad JOIN that produces duplicates, fix the JOIN instead.</p>
"""
    },
    {
        "id": 18,
        "category": "Distinct & Dedup",
        "title": "COUNT DISTINCT",
        "description": "How many unique cities do our customers come from?",
        "tables_used": ["customers"],
        "starter_sql": "SELECT COUNT(DISTINCT -- column)\nFROM customers;",
        "solution_sql": "SELECT COUNT(DISTINCT city) AS unique_cities\nFROM customers;",
        "explanation": """
<h3>COUNT(DISTINCT col)</h3>
<p>Combines COUNT with DISTINCT to count the number of unique non-NULL values in a column. This is different from <code>COUNT(*)</code> which counts all rows.</p>
<pre>COUNT(*)           -- total rows = 15
COUNT(city)        -- non-NULL city values = 15
COUNT(DISTINCT city) -- unique cities = fewer</pre>
"""
    },

    # ─────────────────────────────────────────
    # GROUP BY & HAVING
    # ─────────────────────────────────────────
    {
        "id": 19,
        "category": "Group By & Having",
        "title": "HAVING to Filter Groups",
        "description": "Find departments that have more than 3 employees.",
        "tables_used": ["employees"],
        "starter_sql": "SELECT department_id, COUNT(*) AS num_employees\nFROM employees\nGROUP BY department_id\nHAVING -- filter condition;",
        "solution_sql": "SELECT department_id,\n       COUNT(*) AS num_employees\nFROM employees\nGROUP BY department_id\nHAVING COUNT(*) > 3\nORDER BY num_employees DESC;",
        "explanation": """
<h3>WHERE vs HAVING</h3>
<table>
  <tr><th></th><th>WHERE</th><th>HAVING</th></tr>
  <tr><td>Filters</td><td>Individual rows</td><td>Groups (after aggregation)</td></tr>
  <tr><td>Runs</td><td>Before GROUP BY</td><td>After GROUP BY</td></tr>
  <tr><td>Can use aggregates?</td><td>No</td><td>Yes</td></tr>
</table>
<p>Think of HAVING as "WHERE for groups". You can reference aggregate functions directly in HAVING.</p>
"""
    },
    {
        "id": 20,
        "category": "Group By & Having",
        "title": "Combined WHERE and HAVING",
        "description": "Among employees hired after 2018, find departments where the average salary exceeds 75,000.",
        "tables_used": ["employees"],
        "starter_sql": "SELECT department_id, ROUND(AVG(salary),2) AS avg_sal\nFROM employees\nWHERE -- filter rows first\nGROUP BY department_id\nHAVING -- filter groups;",
        "solution_sql": "SELECT department_id,\n       ROUND(AVG(salary), 2) AS avg_sal\nFROM employees\nWHERE hire_date > '2018-12-31'\nGROUP BY department_id\nHAVING AVG(salary) > 75000\nORDER BY avg_sal DESC;",
        "explanation": """
<h3>Logical execution order</h3>
<ol>
  <li><strong>FROM</strong> — identify the table</li>
  <li><strong>WHERE</strong> — filter individual rows (hire_date > 2018)</li>
  <li><strong>GROUP BY</strong> — group the surviving rows</li>
  <li><strong>HAVING</strong> — filter groups (avg salary > 75000)</li>
  <li><strong>SELECT</strong> — compute expressions and aliases</li>
  <li><strong>ORDER BY</strong> — sort the result</li>
  <li><strong>LIMIT/OFFSET</strong> — paginate</li>
</ol>
<p>This order explains why you can't use a SELECT alias in WHERE or HAVING — those clauses are evaluated before SELECT aliases exist.</p>
"""
    },
    {
        "id": 21,
        "category": "Group By & Having",
        "title": "Total Sales per Region",
        "description": "Show the total sales amount per region, only for regions where total sales exceed 80,000. Order by total descending.",
        "tables_used": ["sales"],
        "starter_sql": "SELECT region, SUM(amount) AS total\nFROM sales\nGROUP BY -- group\nHAVING -- filter;",
        "solution_sql": "SELECT region,\n       SUM(amount) AS total_sales\nFROM sales\nGROUP BY region\nHAVING SUM(amount) > 80000\nORDER BY total_sales DESC;",
        "explanation": """
<h3>Aggregating with HAVING</h3>
<p>This is a classic reporting query: group data, aggregate it, then filter to show only significant groups.</p>
<p>A common mistake is writing <code>HAVING total_sales > 80000</code> — but the alias <code>total_sales</code> doesn't exist yet when HAVING is evaluated. Always use the actual aggregate expression in HAVING (or use a subquery/CTE).</p>
"""
    },

    # ─────────────────────────────────────────
    # JOINS
    # ─────────────────────────────────────────
    {
        "id": 22,
        "category": "Joins",
        "title": "INNER JOIN",
        "description": "List each employee's name alongside their department name. Only include employees who belong to a department.",
        "tables_used": ["employees", "departments"],
        "starter_sql": "SELECT e.name AS employee, d.name AS department\nFROM employees e\n-- join departments;",
        "solution_sql": "SELECT e.name   AS employee,\n       d.name   AS department,\n       d.location\nFROM employees e\nINNER JOIN departments d ON e.department_id = d.id\nORDER BY d.name, e.name;",
        "explanation": """
<h3>INNER JOIN</h3>
<p>Returns only rows where the join condition matches in <strong>both</strong> tables. Rows in either table that don't have a match are excluded.</p>
<pre>employees ──┐
            ├── matching rows only ──► result
departments ──┘</pre>
<h3>Table aliases</h3>
<p>Use short aliases (<code>e</code>, <code>d</code>) to avoid repeating full table names. The alias is defined in FROM and used everywhere else in the query.</p>
"""
    },
    {
        "id": 23,
        "category": "Joins",
        "title": "LEFT JOIN",
        "description": "List all departments and their employees. Include departments that currently have no employees.",
        "tables_used": ["employees", "departments"],
        "starter_sql": "SELECT d.name AS department, e.name AS employee\nFROM departments d\n-- left join employees;",
        "solution_sql": "SELECT d.name  AS department,\n       e.name  AS employee,\n       e.salary\nFROM departments d\nLEFT JOIN employees e ON d.id = e.department_id\nORDER BY d.name, e.name;",
        "explanation": """
<h3>LEFT JOIN (LEFT OUTER JOIN)</h3>
<p>Returns <strong>all rows from the left table</strong>, plus matching rows from the right table. When there is no match, the right table's columns are filled with NULL.</p>
<pre>departments (left) ──► ALL rows in result
employees (right)  ──► NULLs where no match</pre>
<p>Use LEFT JOIN when you want to preserve all records from one side regardless of whether a match exists — e.g., "show all departments even if they're empty".</p>
"""
    },
    {
        "id": 24,
        "category": "Joins",
        "title": "SELF JOIN",
        "description": "List each employee alongside their manager's name. Exclude employees with no manager.",
        "tables_used": ["employees"],
        "starter_sql": "SELECT e.name AS employee, -- manager name\nFROM employees e\n-- self join for manager;",
        "solution_sql": "SELECT e.name  AS employee,\n       m.name  AS manager\nFROM employees e\nINNER JOIN employees m ON e.manager_id = m.id\nORDER BY manager, employee;",
        "explanation": """
<h3>SELF JOIN</h3>
<p>A self join joins a table to itself. This is used for hierarchical data like org charts, categories with subcategories, or sequences where a row references another row in the same table.</p>
<p>You <strong>must</strong> use different aliases for the two "copies" of the table (here <code>e</code> for employee and <code>m</code> for manager), otherwise the database doesn't know which copy you're referring to.</p>
<pre>-- To include employees without a manager (NULL manager_id):
FROM employees e LEFT JOIN employees m ON e.manager_id = m.id</pre>
"""
    },
    {
        "id": 25,
        "category": "Joins",
        "title": "Multi-table JOIN",
        "description": "Show each order with: customer name, product name, quantity, and total amount.",
        "tables_used": ["orders", "customers", "products"],
        "starter_sql": "SELECT -- columns\nFROM orders o\n-- join customers and products;",
        "solution_sql": "SELECT c.name   AS customer,\n       p.name   AS product,\n       o.quantity,\n       o.total_amount\nFROM orders o\nINNER JOIN customers c ON o.customer_id = c.id\nINNER JOIN products  p ON o.product_id  = p.id\nORDER BY o.order_date;",
        "explanation": """
<h3>Chaining multiple JOINs</h3>
<p>You can chain as many JOINs as needed. Each JOIN adds columns from another table. The database processes them sequentially (logically):</p>
<ol>
  <li><code>orders</code> joined with <code>customers</code> → gives customer name</li>
  <li>Result joined with <code>products</code> → gives product name</li>
</ol>
<p>Tip: Always qualify column names with the table alias when joining multiple tables to avoid ambiguity (e.g., <code>o.quantity</code> not just <code>quantity</code>).</p>
"""
    },
    {
        "id": 26,
        "category": "Joins",
        "title": "JOIN with Aggregate",
        "description": "For each department, show the department name (not just the ID), the number of employees, and the total salary. Sort by total salary descending.",
        "tables_used": ["employees", "departments"],
        "starter_sql": "SELECT d.name, -- aggregates\nFROM employees e\nJOIN departments d ON -- condition\nGROUP BY -- group;",
        "solution_sql": "SELECT d.name          AS department,\n       COUNT(e.id)    AS num_employees,\n       SUM(e.salary)  AS total_salary\nFROM departments d\nLEFT JOIN employees e ON d.id = e.department_id\nGROUP BY d.id, d.name\nORDER BY total_salary DESC;",
        "explanation": """
<h3>JOIN + GROUP BY</h3>
<p>Combining JOINs with GROUP BY is extremely common in reporting. The pattern is:</p>
<ol>
  <li>JOIN the tables to bring in descriptive names</li>
  <li>GROUP BY the identifying column</li>
  <li>Apply aggregate functions</li>
</ol>
<p>We use LEFT JOIN so departments with zero employees still appear (with COUNT = 0). Using INNER JOIN would silently drop empty departments.</p>
<p>When grouping by a table's primary key, you can also include any other column from that table in the SELECT without adding it to GROUP BY (because the PK uniquely determines the row).</p>
"""
    },

    # ─────────────────────────────────────────
    # SUBQUERIES
    # ─────────────────────────────────────────
    {
        "id": 27,
        "category": "Subqueries",
        "title": "Scalar Subquery",
        "description": "Find all employees who earn more than the company-wide average salary.",
        "tables_used": ["employees"],
        "starter_sql": "SELECT name, salary\nFROM employees\nWHERE salary > (-- subquery for avg);",
        "solution_sql": "SELECT name, salary\nFROM employees\nWHERE salary > (SELECT AVG(salary) FROM employees)\nORDER BY salary DESC;",
        "explanation": """
<h3>Scalar subquery</h3>
<p>A scalar subquery returns a <strong>single value</strong> (one row, one column). It can be used anywhere a single value is expected: in WHERE, SELECT, HAVING, etc.</p>
<pre>SELECT AVG(salary) FROM employees  →  returns e.g. 75550</pre>
<p>The outer query then uses that number: <code>WHERE salary &gt; 75550</code>.</p>
<p>The subquery is evaluated once and the result is reused — efficient for static values. For row-by-row comparison, you need a correlated subquery.</p>
"""
    },
    {
        "id": 28,
        "category": "Subqueries",
        "title": "IN with Subquery",
        "description": "Find all customers who have placed at least one order.",
        "tables_used": ["customers", "orders"],
        "starter_sql": "SELECT name\nFROM customers\nWHERE id IN (-- subquery);",
        "solution_sql": "SELECT name, city, country\nFROM customers\nWHERE id IN (\n    SELECT DISTINCT customer_id\n    FROM orders\n)\nORDER BY name;",
        "explanation": """
<h3>IN with subquery</h3>
<p>The subquery returns a list of values; the outer query checks if each row's column appears in that list. Equivalent to an INNER JOIN but sometimes clearer in intent.</p>
<pre>-- Equivalent using JOIN:
SELECT DISTINCT c.name, c.city
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id;</pre>
<p>Use <code>NOT IN</code> to find customers who have NOT placed any orders — but be careful: if the subquery returns any NULL, <code>NOT IN</code> returns no rows! Use <code>NOT EXISTS</code> instead when NULLs are possible.</p>
"""
    },
    {
        "id": 29,
        "category": "Subqueries",
        "title": "Correlated Subquery",
        "description": "For each employee, show their name, salary, and whether their salary is above their department's average (show 'Yes' or 'No').",
        "tables_used": ["employees"],
        "starter_sql": "SELECT name, salary, department_id,\n  -- correlated subquery for dept avg\nFROM employees;",
        "solution_sql": "SELECT e.name,\n       e.salary,\n       e.department_id,\n       ROUND((SELECT AVG(salary)\n              FROM employees\n              WHERE department_id = e.department_id), 2) AS dept_avg,\n       CASE WHEN e.salary > (SELECT AVG(salary)\n                              FROM employees\n                              WHERE department_id = e.department_id)\n            THEN 'Yes' ELSE 'No'\n       END AS above_dept_avg\nFROM employees e\nORDER BY e.department_id, e.salary DESC;",
        "explanation": """
<h3>Correlated subquery</h3>
<p>A correlated subquery references columns from the outer query (<code>e.department_id</code> here). It is <strong>re-executed once for every row</strong> of the outer query — so it's slower than a scalar subquery but very powerful for row-by-row comparisons.</p>
<h3>CASE WHEN</h3>
<p><code>CASE WHEN condition THEN result ELSE fallback END</code> is SQL's if/else. It produces a value for each row based on conditions — great for labeling, bucketing, and conditional aggregation.</p>
<p><strong>Performance tip:</strong> Correlated subqueries can be slow on large tables. Often a JOIN or window function is more efficient:</p>
<pre>-- Window function alternative (faster):
AVG(salary) OVER (PARTITION BY department_id) AS dept_avg</pre>
"""
    },
    {
        "id": 30,
        "category": "Subqueries",
        "title": "EXISTS Subquery",
        "description": "Find all customers who have NEVER placed an order.",
        "tables_used": ["customers", "orders"],
        "starter_sql": "SELECT name\nFROM customers\nWHERE NOT EXISTS (-- subquery);",
        "solution_sql": "SELECT c.name, c.email, c.city\nFROM customers c\nWHERE NOT EXISTS (\n    SELECT 1\n    FROM orders o\n    WHERE o.customer_id = c.id\n)\nORDER BY c.name;",
        "explanation": """
<h3>EXISTS vs IN</h3>
<table>
  <tr><th>Feature</th><th>IN</th><th>EXISTS</th></tr>
  <tr><td>Returns</td><td>List of values</td><td>TRUE/FALSE per row</td></tr>
  <tr><td>NULL safe?</td><td>No — NOT IN fails with NULLs</td><td>Yes</td></tr>
  <tr><td>Short-circuits?</td><td>No</td><td>Yes — stops at first match</td></tr>
  <tr><td>Best for</td><td>Small fixed lists</td><td>Large tables, correlated checks</td></tr>
</table>
<p><code>SELECT 1</code> inside EXISTS is a convention — the actual value doesn't matter, only whether a row exists. EXISTS returns TRUE as soon as one matching row is found.</p>
"""
    },

    # ─────────────────────────────────────────
    # WINDOW FUNCTIONS
    # ─────────────────────────────────────────
    {
        "id": 31,
        "category": "Window Functions",
        "title": "ROW_NUMBER",
        "description": "Assign a unique sequential number to each employee within their department, ordered by salary descending.",
        "tables_used": ["employees"],
        "starter_sql": "SELECT name, department_id, salary,\n  ROW_NUMBER() OVER (-- partition and order)\nFROM employees;",
        "solution_sql": "SELECT name,\n       department_id,\n       salary,\n       ROW_NUMBER() OVER (\n           PARTITION BY department_id\n           ORDER BY salary DESC\n       ) AS row_num\nFROM employees\nORDER BY department_id, salary DESC;",
        "explanation": """
<h3>Window functions</h3>
<p>A window function computes a value across a set of rows related to the current row — without collapsing them into groups (unlike GROUP BY). The <code>OVER()</code> clause defines the "window" (the related rows).</p>
<h3>ROW_NUMBER()</h3>
<p>Assigns a strictly unique integer (1, 2, 3...) per partition. Even if two rows have identical salary, they get different row numbers — the tie-breaking order is arbitrary.</p>
<h3>PARTITION BY</h3>
<p>Divides rows into groups (partitions). The window function restarts its counter for each partition. Omitting PARTITION BY means the entire result set is one partition.</p>
"""
    },
    {
        "id": 32,
        "category": "Window Functions",
        "title": "RANK vs DENSE_RANK",
        "description": "Rank all employees by salary (highest first) company-wide. Show both RANK and DENSE_RANK to see the difference.",
        "tables_used": ["employees"],
        "starter_sql": "SELECT name, salary,\n  RANK() OVER (ORDER BY salary DESC) AS rnk,\n  DENSE_RANK() OVER (-- same) AS dense_rnk\nFROM employees;",
        "solution_sql": "SELECT name,\n       salary,\n       RANK()       OVER (ORDER BY salary DESC) AS rnk,\n       DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rnk\nFROM employees\nORDER BY salary DESC;",
        "explanation": """
<h3>RANK vs DENSE_RANK</h3>
<table>
  <tr><th>Function</th><th>Ties get same rank?</th><th>Gap after tie?</th></tr>
  <tr><td>ROW_NUMBER()</td><td>No — always unique</td><td>N/A</td></tr>
  <tr><td>RANK()</td><td>Yes</td><td>Yes — skips numbers</td></tr>
  <tr><td>DENSE_RANK()</td><td>Yes</td><td>No — sequential</td></tr>
</table>
<p>Example with salaries 100, 100, 80:</p>
<pre>salary  ROW_NUMBER  RANK  DENSE_RANK
100       1           1      1
100       2           1      1
80        3           3      2   ← RANK skips 2, DENSE_RANK doesn't</pre>
<p>Use DENSE_RANK when you want "top 3 salary levels" regardless of how many employees share a rank.</p>
"""
    },
    {
        "id": 33,
        "category": "Window Functions",
        "title": "LAG and LEAD",
        "description": "For each sale, show the current amount and the previous sale amount for the same employee (ordered by date). Calculate the difference.",
        "tables_used": ["sales"],
        "starter_sql": "SELECT employee_id, sale_date, amount,\n  LAG(amount) OVER (-- partition by employee, order by date)\nFROM sales;",
        "solution_sql": "SELECT employee_id,\n       sale_date,\n       amount,\n       LAG(amount)  OVER (PARTITION BY employee_id ORDER BY sale_date) AS prev_amount,\n       amount - LAG(amount) OVER (PARTITION BY employee_id ORDER BY sale_date) AS change\nFROM sales\nORDER BY employee_id, sale_date;",
        "explanation": """
<h3>LAG and LEAD</h3>
<ul>
  <li><code>LAG(col, n, default)</code> — value from <em>n</em> rows <strong>before</strong> the current row (default n=1)</li>
  <li><code>LEAD(col, n, default)</code> — value from <em>n</em> rows <strong>after</strong> the current row</li>
</ul>
<p>When there is no previous row (first row of a partition), LAG returns NULL by default. You can provide a fallback: <code>LAG(amount, 1, 0)</code> returns 0 instead of NULL.</p>
<p>Common uses: month-over-month growth, period comparisons, detecting streaks, finding next/previous events.</p>
"""
    },
    {
        "id": 34,
        "category": "Window Functions",
        "title": "Running Total with SUM OVER",
        "description": "Show each sale with a running total of sales for that employee (cumulative sum ordered by date).",
        "tables_used": ["sales"],
        "starter_sql": "SELECT employee_id, sale_date, amount,\n  SUM(amount) OVER (-- running total per employee)\nFROM sales;",
        "solution_sql": "SELECT employee_id,\n       sale_date,\n       amount,\n       SUM(amount) OVER (\n           PARTITION BY employee_id\n           ORDER BY sale_date\n           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW\n       ) AS running_total\nFROM sales\nORDER BY employee_id, sale_date;",
        "explanation": """
<h3>Window frame</h3>
<p>The <strong>frame clause</strong> specifies which rows within the partition contribute to the window function:</p>
<pre>ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW</pre>
<p>This means: from the very first row of the partition to the current row — a classic running total.</p>
<h3>Other frame examples</h3>
<ul>
  <li><code>ROWS BETWEEN 2 PRECEDING AND CURRENT ROW</code> — 3-row rolling average</li>
  <li><code>ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING</code> — reverse running total</li>
  <li><code>ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING</code> — full partition (same as omitting ORDER BY in frame)</li>
</ul>
<p>When you use ORDER BY inside OVER() without a frame clause, the default frame is <code>RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW</code>, which produces a running total but treats ties differently from ROWS.</p>
"""
    },
    {
        "id": 35,
        "category": "Window Functions",
        "title": "NTILE — Salary Quartiles",
        "description": "Divide all employees into 4 salary quartiles (1 = top earners, 4 = lowest earners). Show each employee with their quartile.",
        "tables_used": ["employees"],
        "starter_sql": "SELECT name, salary,\n  NTILE(4) OVER (ORDER BY salary DESC) AS quartile\nFROM employees\nORDER BY salary DESC;",
        "solution_sql": "SELECT name,\n       salary,\n       NTILE(4) OVER (ORDER BY salary DESC) AS quartile,\n       CASE NTILE(4) OVER (ORDER BY salary DESC)\n           WHEN 1 THEN 'Top 25%'\n           WHEN 2 THEN 'Upper-mid'\n           WHEN 3 THEN 'Lower-mid'\n           WHEN 4 THEN 'Bottom 25%'\n       END AS salary_band\nFROM employees\nORDER BY salary DESC;",
        "explanation": """
<h3>NTILE(n)</h3>
<p>Divides the rows into <em>n</em> buckets as evenly as possible. Useful for percentiles, quartiles, and deciles.</p>
<ul>
  <li><code>NTILE(2)</code> → median split (above/below median)</li>
  <li><code>NTILE(4)</code> → quartiles (Q1–Q4)</li>
  <li><code>NTILE(100)</code> → percentile rank</li>
</ul>
<p>If the rows don't divide evenly, the earlier buckets get one extra row.</p>
"""
    },

    # ─────────────────────────────────────────
    # CTEs
    # ─────────────────────────────────────────
    {
        "id": 36,
        "category": "CTEs",
        "title": "Basic CTE",
        "description": "Use a CTE to find the average salary per department, then show only departments where the average is above the overall company average.",
        "tables_used": ["employees"],
        "starter_sql": "WITH dept_avg AS (\n  -- subquery here\n)\nSELECT *\nFROM dept_avg\nWHERE -- filter;",
        "solution_sql": "WITH dept_avg AS (\n    SELECT department_id,\n           ROUND(AVG(salary), 2) AS avg_salary\n    FROM employees\n    GROUP BY department_id\n)\nSELECT department_id, avg_salary\nFROM dept_avg\nWHERE avg_salary > (SELECT AVG(salary) FROM employees)\nORDER BY avg_salary DESC;",
        "explanation": """
<h3>CTE (Common Table Expression)</h3>
<p>A CTE is a named temporary result set defined at the top of a query with <code>WITH name AS (...)</code>. It can be referenced by name in the main query.</p>
<h3>Why use CTEs?</h3>
<ul>
  <li><strong>Readability:</strong> Break complex logic into named, digestible steps</li>
  <li><strong>Reusability:</strong> Reference the same CTE multiple times in one query</li>
  <li><strong>Debugging:</strong> Easy to test each CTE in isolation</li>
  <li><strong>Replaces nested subqueries:</strong> Avoids deeply indented subqueries</li>
</ul>
<p>Multiple CTEs: <code>WITH cte1 AS (...), cte2 AS (...) SELECT ...</code></p>
"""
    },
    {
        "id": 37,
        "category": "CTEs",
        "title": "Multi-step CTE",
        "description": "Using CTEs: first find the top-selling employee per region, then join with the employees table to show their names.",
        "tables_used": ["sales", "employees"],
        "starter_sql": "WITH regional_totals AS (\n  -- total sales per employee per region\n),\ntop_per_region AS (\n  -- highest total per region\n)\nSELECT -- final result;",
        "solution_sql": "WITH regional_totals AS (\n    SELECT employee_id,\n           region,\n           SUM(amount) AS total\n    FROM sales\n    GROUP BY employee_id, region\n),\nranked AS (\n    SELECT *,\n           RANK() OVER (PARTITION BY region ORDER BY total DESC) AS rnk\n    FROM regional_totals\n)\nSELECT r.region,\n       e.name AS top_employee,\n       r.total\nFROM ranked r\nINNER JOIN employees e ON r.employee_id = e.id\nWHERE r.rnk = 1\nORDER BY r.region;",
        "explanation": """
<h3>Chaining CTEs</h3>
<p>Each CTE can reference earlier CTEs in the chain. This lets you build complex analytics step by step:</p>
<ol>
  <li><code>regional_totals</code> — aggregate sales by employee + region</li>
  <li><code>ranked</code> — rank employees within each region by their total</li>
  <li>Main query — filter to rank 1 (top employee per region) and join for names</li>
</ol>
<p>This is cleaner than nesting three levels of subqueries. The optimizer typically treats CTEs identically to subqueries (in SQLite they are inlined).</p>
"""
    },

    # ─────────────────────────────────────────
    # SET OPERATIONS
    # ─────────────────────────────────────────
    {
        "id": 38,
        "category": "Set Operations",
        "title": "UNION ALL",
        "description": "Combine the list of employee names from department 1 AND department 2 into a single list. Keep duplicates if any.",
        "tables_used": ["employees"],
        "starter_sql": "SELECT name FROM employees WHERE department_id = 1\nUNION ALL\nSELECT -- second set;",
        "solution_sql": "SELECT name, 'Engineering' AS dept FROM employees WHERE department_id = 1\nUNION ALL\nSELECT name, 'Marketing'   AS dept FROM employees WHERE department_id = 2\nORDER BY dept, name;",
        "explanation": """
<h3>UNION vs UNION ALL</h3>
<table>
  <tr><th></th><th>UNION</th><th>UNION ALL</th></tr>
  <tr><td>Duplicates</td><td>Removed</td><td>Kept</td></tr>
  <tr><td>Performance</td><td>Slower (requires sort/hash to dedup)</td><td>Faster</td></tr>
  <tr><td>Use when</td><td>You need distinct rows</td><td>All rows or no duplicates possible</td></tr>
</table>
<h3>Rules for UNION</h3>
<ul>
  <li>Both queries must have the same number of columns</li>
  <li>Corresponding columns must have compatible types</li>
  <li>Column names come from the first SELECT</li>
  <li>Only one ORDER BY at the end (applies to the combined result)</li>
</ul>
"""
    },
    {
        "id": 39,
        "category": "Set Operations",
        "title": "INTERSECT",
        "description": "Find cities that appear in both the customers table AND the departments table (locations).",
        "tables_used": ["customers", "departments"],
        "starter_sql": "SELECT city FROM customers\nINTERSECT\nSELECT -- from departments;",
        "solution_sql": "SELECT city    AS common_location FROM customers\nINTERSECT\nSELECT location AS common_location FROM departments\nORDER BY common_location;",
        "explanation": """
<h3>INTERSECT</h3>
<p>Returns only rows that appear in <strong>both</strong> result sets (the intersection). Duplicates are automatically removed.</p>
<p>Equivalent to:</p>
<pre>SELECT DISTINCT city FROM customers c
WHERE EXISTS (
    SELECT 1 FROM departments d WHERE d.location = c.city
)</pre>
<p>Note: SQLite supports INTERSECT. Not all databases support INTERSECT ALL (which keeps duplicates).</p>
"""
    },
    {
        "id": 40,
        "category": "Set Operations",
        "title": "EXCEPT",
        "description": "Find customers who have placed orders but whose total spending is less than 500. Use EXCEPT to find customers in the ordered set but not in the high-spenders set.",
        "tables_used": ["orders", "customers"],
        "starter_sql": "-- customers who ordered\nSELECT customer_id FROM orders\nEXCEPT\n-- customers who spent >= 500\nSELECT -- high spenders;",
        "solution_sql": "SELECT customer_id FROM orders\nEXCEPT\nSELECT customer_id\nFROM orders\nGROUP BY customer_id\nHAVING SUM(total_amount) >= 500;",
        "explanation": """
<h3>EXCEPT (MINUS in Oracle)</h3>
<p>Returns rows from the first query that do <strong>not</strong> appear in the second query. Like INTERSECT, it removes duplicates.</p>
<pre>Set A EXCEPT Set B = A - B (rows in A but not in B)</pre>
<p>This is a clean way to express "find X but not Y" patterns without NOT IN or NOT EXISTS.</p>
"""
    },

    # ─────────────────────────────────────────
    # STRING FUNCTIONS
    # ─────────────────────────────────────────
    {
        "id": 41,
        "category": "String Functions",
        "title": "String Manipulation",
        "description": "Display each customer's name in uppercase, their email domain (part after @), and the length of their name.",
        "tables_used": ["customers"],
        "starter_sql": "SELECT\n  UPPER(name) AS upper_name,\n  -- extract domain from email\n  LENGTH(name) AS name_length\nFROM customers;",
        "solution_sql": "SELECT\n  UPPER(name)                                    AS upper_name,\n  SUBSTR(email, INSTR(email, '@') + 1)           AS email_domain,\n  LENGTH(name)                                   AS name_length\nFROM customers\nORDER BY name_length DESC;",
        "explanation": """
<h3>Common string functions (SQLite)</h3>
<table>
  <tr><th>Function</th><th>Description</th></tr>
  <tr><td>UPPER(s)</td><td>Convert to uppercase</td></tr>
  <tr><td>LOWER(s)</td><td>Convert to lowercase</td></tr>
  <tr><td>LENGTH(s)</td><td>Number of characters</td></tr>
  <tr><td>SUBSTR(s, start, len)</td><td>Extract substring (1-indexed)</td></tr>
  <tr><td>INSTR(s, sub)</td><td>Position of first occurrence of sub in s (0 if not found)</td></tr>
  <tr><td>TRIM(s)</td><td>Remove leading/trailing whitespace</td></tr>
  <tr><td>REPLACE(s, old, new)</td><td>Replace all occurrences</td></tr>
  <tr><td>s1 || s2</td><td>Concatenate strings (use || in SQLite)</td></tr>
</table>
"""
    },
    {
        "id": 42,
        "category": "String Functions",
        "title": "CASE with String Categorization",
        "description": "Categorize each product by price: 'Budget' (< 50), 'Mid-range' (50–200), 'Premium' (> 200). Show product name, price, and category label.",
        "tables_used": ["products"],
        "starter_sql": "SELECT name, price,\n  CASE\n    -- conditions\n  END AS price_category\nFROM products;",
        "solution_sql": "SELECT name,\n       price,\n       CASE\n           WHEN price < 50    THEN 'Budget'\n           WHEN price <= 200  THEN 'Mid-range'\n           ELSE                    'Premium'\n       END AS price_category\nFROM products\nORDER BY price;",
        "explanation": """
<h3>Searched CASE expression</h3>
<pre>CASE
  WHEN condition1 THEN result1
  WHEN condition2 THEN result2
  ELSE default_result
END</pre>
<p>Conditions are evaluated top to bottom; the first TRUE condition wins. If no condition matches and there's no ELSE, the result is NULL.</p>
<h3>Simple CASE expression</h3>
<pre>CASE col
  WHEN 'A' THEN 'Excellent'
  WHEN 'B' THEN 'Good'
  ELSE 'Other'
END</pre>
<p>The simple form tests equality against one column. The searched form allows any condition.</p>
"""
    },

    # ─────────────────────────────────────────
    # DATE FUNCTIONS
    # ─────────────────────────────────────────
    {
        "id": 43,
        "category": "Date Functions",
        "title": "Extract Year / Month",
        "description": "Show the number of orders placed per month in 2023. Use STRFTIME to extract year and month.",
        "tables_used": ["orders"],
        "starter_sql": "SELECT\n  STRFTIME('%Y-%m', order_date) AS month,\n  COUNT(*) AS num_orders\nFROM orders\nWHERE -- filter 2023\nGROUP BY -- group\nORDER BY month;",
        "solution_sql": "SELECT\n  STRFTIME('%Y-%m', order_date) AS month,\n  COUNT(*)                      AS num_orders,\n  SUM(total_amount)             AS monthly_revenue\nFROM orders\nWHERE STRFTIME('%Y', order_date) = '2023'\nGROUP BY STRFTIME('%Y-%m', order_date)\nORDER BY month;",
        "explanation": """
<h3>STRFTIME in SQLite</h3>
<p>SQLite stores dates as text ('YYYY-MM-DD'). <code>STRFTIME(format, date)</code> extracts parts of a date:</p>
<table>
  <tr><th>Format</th><th>Returns</th></tr>
  <tr><td>%Y</td><td>4-digit year</td></tr>
  <tr><td>%m</td><td>Month (01–12)</td></tr>
  <tr><td>%d</td><td>Day (01–31)</td></tr>
  <tr><td>%H</td><td>Hour (00–23)</td></tr>
  <tr><td>%Y-%m</td><td>Year-Month (e.g. 2023-06)</td></tr>
</table>
<p>In other databases: use <code>YEAR(date)</code> / <code>MONTH(date)</code> (MySQL), or <code>EXTRACT(YEAR FROM date)</code> (PostgreSQL / standard SQL).</p>
"""
    },
    {
        "id": 44,
        "category": "Date Functions",
        "title": "Date Arithmetic",
        "description": "Calculate the tenure (in years) of each employee based on their hire date and today's date. Show employees with 5+ years of tenure.",
        "tables_used": ["employees"],
        "starter_sql": "SELECT name, hire_date,\n  -- compute years of tenure\nFROM employees\nWHERE -- 5+ years;",
        "solution_sql": "SELECT name,\n       hire_date,\n       CAST(\n           (JULIANDAY(DATE('now')) - JULIANDAY(hire_date)) / 365.25\n       AS INTEGER) AS tenure_years\nFROM employees\nWHERE (JULIANDAY(DATE('now')) - JULIANDAY(hire_date)) / 365.25 >= 5\nORDER BY hire_date;",
        "explanation": """
<h3>JULIANDAY and date arithmetic</h3>
<p><code>JULIANDAY(date)</code> converts a date to a floating-point Julian Day Number. Subtracting two Julian Day values gives the difference in days.</p>
<p>Dividing by 365.25 (average year length) converts to years.</p>
<h3>DATE('now')</h3>
<p>Returns today's date in 'YYYY-MM-DD' format. The result of this query will vary depending on when you run it.</p>
<p>In PostgreSQL: <code>AGE(NOW(), hire_date)</code> or <code>DATE_PART('year', AGE(hire_date))</code></p>
<p>In MySQL: <code>TIMESTAMPDIFF(YEAR, hire_date, NOW())</code></p>
"""
    },

    # ─────────────────────────────────────────
    # NULL HANDLING
    # ─────────────────────────────────────────
    {
        "id": 45,
        "category": "NULL Handling",
        "title": "COALESCE",
        "description": "Display each employee with their manager's ID. If they have no manager (NULL), show the text 'Top-level manager' instead.",
        "tables_used": ["employees"],
        "starter_sql": "SELECT name,\n  COALESCE(-- handle null manager_id)\nFROM employees;",
        "solution_sql": "SELECT name,\n       COALESCE(CAST(manager_id AS TEXT), 'Top-level manager') AS manager_info\nFROM employees\nORDER BY manager_id NULLS LAST;",
        "explanation": """
<h3>COALESCE(val1, val2, ...)</h3>
<p>Returns the first non-NULL value in the list. If all values are NULL, returns NULL.</p>
<pre>COALESCE(NULL, NULL, 'fallback') → 'fallback'
COALESCE(5,    NULL, 'fallback') → 5</pre>
<p>Common use cases:</p>
<ul>
  <li>Provide a default when a column is NULL</li>
  <li>Choose between two columns: <code>COALESCE(phone, email)</code> — use phone, fall back to email</li>
  <li>Turn NULL into 0 in calculations: <code>COALESCE(discount, 0)</code></li>
</ul>
<h3>IFNULL (SQLite-specific)</h3>
<p><code>IFNULL(val, default)</code> is SQLite's two-argument version of COALESCE. Prefer COALESCE for portability.</p>
"""
    },
    {
        "id": 46,
        "category": "NULL Handling",
        "title": "NULLIF",
        "description": "Calculate the average order value per customer. Use NULLIF to avoid division by zero if somehow quantity is 0.",
        "tables_used": ["orders"],
        "starter_sql": "SELECT customer_id,\n  SUM(total_amount) / NULLIF(COUNT(*), 0) AS avg_order_value\nFROM orders\nGROUP BY customer_id;",
        "solution_sql": "SELECT customer_id,\n       COUNT(*)                                        AS num_orders,\n       SUM(total_amount)                               AS total_spent,\n       ROUND(SUM(total_amount) / NULLIF(COUNT(*), 0), 2) AS avg_order_value\nFROM orders\nGROUP BY customer_id\nORDER BY total_spent DESC;",
        "explanation": """
<h3>NULLIF(val, compare)</h3>
<p><code>NULLIF(a, b)</code> returns NULL if <code>a = b</code>, otherwise returns <code>a</code>.</p>
<p>Its main use is <strong>safe division</strong>: <code>numerator / NULLIF(denominator, 0)</code>. If the denominator is 0, NULLIF returns NULL, and dividing by NULL gives NULL — no division-by-zero error.</p>
<pre>10 / NULLIF(2, 0)  → 5
10 / NULLIF(0, 0)  → NULL  (not an error)</pre>
"""
    },

    # ─────────────────────────────────────────
    # DDL & INDEXES
    # ─────────────────────────────────────────
    {
        "id": 47,
        "category": "DDL & Indexes",
        "title": "CREATE TABLE Statement",
        "description": "Write a CREATE TABLE statement for a new <code>reviews</code> table (not executed — shown for learning). Columns: id (PK), product_id (FK), customer_id (FK), rating (1–5), comment (text, optional), review_date.",
        "tables_used": [],
        "starter_sql": "-- This is a DDL example (not executable in this sandbox)\n-- Write the CREATE TABLE statement:\nCREATE TABLE reviews (\n  -- columns here\n);",
        "solution_sql": "-- DDL example (read-only sandbox — for learning purposes)\nCREATE TABLE reviews (\n    id          INTEGER PRIMARY KEY AUTOINCREMENT,\n    product_id  INTEGER NOT NULL REFERENCES products(id),\n    customer_id INTEGER NOT NULL REFERENCES customers(id),\n    rating      INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),\n    comment     TEXT,\n    review_date TEXT NOT NULL DEFAULT (DATE('now'))\n);",
        "explanation": """
<h3>CREATE TABLE clauses</h3>
<ul>
  <li><code>PRIMARY KEY</code> — uniquely identifies each row; implicitly NOT NULL</li>
  <li><code>AUTOINCREMENT</code> — auto-generates the next integer (SQLite)</li>
  <li><code>NOT NULL</code> — column must always have a value</li>
  <li><code>REFERENCES table(col)</code> — foreign key constraint</li>
  <li><code>CHECK (condition)</code> — validates data on insert/update</li>
  <li><code>DEFAULT value</code> — used when no value is provided on insert</li>
  <li><code>UNIQUE</code> — no two rows can have the same value in this column</li>
</ul>
<h3>Data types in SQLite</h3>
<p>SQLite uses dynamic typing. Common type affinities: <code>INTEGER</code>, <code>REAL</code>, <code>TEXT</code>, <code>BLOB</code>, <code>NUMERIC</code>.</p>
"""
    },
    {
        "id": 48,
        "category": "DDL & Indexes",
        "title": "CREATE and DROP INDEX",
        "description": "Write statements to create an index on <code>orders.customer_id</code> to speed up lookups, and a composite index on <code>sales(employee_id, sale_date)</code>. Also show how to drop an index.",
        "tables_used": [],
        "starter_sql": "-- Create single-column index\nCREATE INDEX -- ...\n\n-- Create composite index\nCREATE INDEX -- ...\n\n-- Drop an index\nDROP INDEX -- ...;",
        "solution_sql": "-- Single-column index on orders.customer_id\nCREATE INDEX idx_orders_customer_id\n    ON orders (customer_id);\n\n-- Composite index (covers both employee_id and date range queries)\nCREATE INDEX idx_sales_emp_date\n    ON sales (employee_id, sale_date);\n\n-- Unique index (enforces uniqueness too)\nCREATE UNIQUE INDEX idx_customers_email\n    ON customers (email);\n\n-- Drop an index\nDROP INDEX IF EXISTS idx_orders_customer_id;",
        "explanation": """
<h3>When indexes help</h3>
<ul>
  <li>Columns used in WHERE, JOIN ON, ORDER BY, GROUP BY</li>
  <li>Foreign key columns (speeds up joins)</li>
  <li>High-cardinality columns (many unique values)</li>
</ul>
<h3>Composite index column order matters</h3>
<p>For <code>CREATE INDEX ON sales (employee_id, sale_date)</code>:</p>
<ul>
  <li>Speeds up: <code>WHERE employee_id = ?</code></li>
  <li>Speeds up: <code>WHERE employee_id = ? AND sale_date &gt; ?</code></li>
  <li>Does NOT help: <code>WHERE sale_date &gt; ?</code> (leading column missing)</li>
</ul>
<p>This is called the <strong>leftmost prefix rule</strong>.</p>
<h3>Cost of indexes</h3>
<p>Each index slows down INSERT/UPDATE/DELETE because the index must also be updated. Don't over-index write-heavy tables.</p>
"""
    },

    # ─────────────────────────────────────────
    # ADVANCED / MIXED
    # ─────────────────────────────────────────
    {
        "id": 49,
        "category": "Advanced",
        "title": "Conditional Aggregation",
        "description": "In one query, show per department: total employees, number of female employees, number of male employees, and the percentage female.",
        "tables_used": ["employees"],
        "starter_sql": "SELECT department_id,\n  COUNT(*) AS total,\n  -- conditional counts for F and M\nFROM employees\nGROUP BY department_id;",
        "solution_sql": "SELECT department_id,\n       COUNT(*)                                        AS total,\n       SUM(CASE WHEN gender = 'F' THEN 1 ELSE 0 END)   AS female_count,\n       SUM(CASE WHEN gender = 'M' THEN 1 ELSE 0 END)   AS male_count,\n       ROUND(\n           100.0 * SUM(CASE WHEN gender = 'F' THEN 1 ELSE 0 END)\n           / COUNT(*), 1\n       )                                               AS pct_female\nFROM employees\nGROUP BY department_id\nORDER BY department_id;",
        "explanation": """
<h3>Conditional aggregation (PIVOT pattern)</h3>
<p>Wrapping CASE inside SUM or COUNT lets you aggregate different subsets of data in a single pass over the table — much more efficient than running multiple queries.</p>
<pre>SUM(CASE WHEN gender = 'F' THEN 1 ELSE 0 END)
-- equivalent to COUNT(*) WHERE gender = 'F'</pre>
<p>This is the standard way to create a pivot table in SQL without a dedicated PIVOT syntax (which only some databases support).</p>
<p>Note: multiplying by <code>100.0</code> (not 100) forces floating-point division. Integer division in SQL truncates: <code>3 / 4 = 0</code>, but <code>3.0 / 4 = 0.75</code>.</p>
"""
    },
    {
        "id": 50,
        "category": "Advanced",
        "title": "Top N per Group",
        "description": "Find the top 2 highest-paid employees in each department.",
        "tables_used": ["employees"],
        "starter_sql": "-- Use ROW_NUMBER or RANK in a CTE\nWITH ranked AS (\n  SELECT *, ROW_NUMBER() OVER (-- window) AS rn\n  FROM employees\n)\nSELECT -- filter top 2;",
        "solution_sql": "WITH ranked AS (\n    SELECT name,\n           department_id,\n           salary,\n           DENSE_RANK() OVER (\n               PARTITION BY department_id\n               ORDER BY salary DESC\n           ) AS rnk\n    FROM employees\n)\nSELECT name, department_id, salary, rnk\nFROM ranked\nWHERE rnk <= 2\nORDER BY department_id, rnk;",
        "explanation": """
<h3>Top-N per group pattern</h3>
<p>This is one of the most common interview questions. The pattern:</p>
<ol>
  <li>Use a window function (ROW_NUMBER / RANK / DENSE_RANK) with <code>PARTITION BY group_col ORDER BY rank_col DESC</code></li>
  <li>Wrap in a CTE or subquery</li>
  <li>Filter where the rank ≤ N</li>
</ol>
<p>DENSE_RANK is preferred here: if two employees tie for rank 1, both appear, and rank 2 is the next distinct salary — you truly get "top 2 salary levels", not just 2 rows.</p>
<p>Using ROW_NUMBER instead arbitrarily excludes one tied employee — fine if you strictly want exactly N rows per group.</p>
"""
    },
    {
        "id": 51,
        "category": "Advanced",
        "title": "Revenue per Customer with Rank",
        "description": "Show each customer's total spending and their rank among all customers by spending. Include the customer name.",
        "tables_used": ["customers", "orders"],
        "starter_sql": "SELECT c.name, SUM(o.total_amount) AS total_spent,\n  RANK() OVER (-- rank by total_spent)\nFROM customers c\nJOIN orders o ON --\nGROUP BY c.id, c.name;",
        "solution_sql": "SELECT c.name,\n       SUM(o.total_amount) AS total_spent,\n       RANK() OVER (ORDER BY SUM(o.total_amount) DESC) AS spending_rank\nFROM customers c\nINNER JOIN orders o ON c.id = o.customer_id\nGROUP BY c.id, c.name\nORDER BY spending_rank;",
        "explanation": """
<h3>Window function over aggregated result</h3>
<p>Window functions are evaluated <em>after</em> GROUP BY and aggregate functions. This means you can use <code>SUM(...)</code> inside <code>OVER(ORDER BY SUM(...))</code>.</p>
<p>Execution order with window functions:</p>
<ol>
  <li>FROM / JOIN</li>
  <li>WHERE</li>
  <li>GROUP BY</li>
  <li>HAVING</li>
  <li>Window functions (OVER)</li>
  <li>SELECT</li>
  <li>DISTINCT</li>
  <li>ORDER BY</li>
  <li>LIMIT</li>
</ol>
<p>Customers with no orders are excluded because we use INNER JOIN. Use LEFT JOIN + COALESCE to include them with 0 spending.</p>
"""
    },
    {
        "id": 52,
        "category": "Advanced",
        "title": "Month-over-Month Growth",
        "description": "Calculate the month-over-month revenue growth for orders. Show each month's revenue, the previous month's revenue, and the growth percentage.",
        "tables_used": ["orders"],
        "starter_sql": "WITH monthly AS (\n  SELECT STRFTIME('%Y-%m', order_date) AS month,\n         SUM(total_amount) AS revenue\n  FROM orders\n  GROUP BY month\n)\nSELECT month, revenue,\n  LAG(revenue) OVER (ORDER BY month) AS prev_revenue,\n  -- growth pct\nFROM monthly;",
        "solution_sql": "WITH monthly AS (\n    SELECT STRFTIME('%Y-%m', order_date) AS month,\n           SUM(total_amount)            AS revenue\n    FROM orders\n    GROUP BY STRFTIME('%Y-%m', order_date)\n)\nSELECT month,\n       ROUND(revenue, 2) AS revenue,\n       ROUND(LAG(revenue) OVER (ORDER BY month), 2) AS prev_month_revenue,\n       CASE\n           WHEN LAG(revenue) OVER (ORDER BY month) IS NULL THEN NULL\n           ELSE ROUND(\n               100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))\n               / LAG(revenue) OVER (ORDER BY month),\n           1)\n       END AS growth_pct\nFROM monthly\nORDER BY month;",
        "explanation": """
<h3>Month-over-month growth pattern</h3>
<p>This combines several concepts:</p>
<ul>
  <li>CTE to pre-aggregate monthly revenue</li>
  <li>LAG to fetch the previous month's revenue</li>
  <li>CASE to handle the first month (no previous month = NULL)</li>
  <li>Formula: <code>(current - previous) / previous * 100</code></li>
</ul>
<p>The first month shows NULL for growth (no prior month to compare). Subsequent months show positive or negative percentages indicating growth or decline.</p>
<p>In production, you'd often handle missing months (months with no orders) by generating a date series and left-joining your data to it.</p>
"""
    },
    {
        "id": 53,
        "category": "Advanced",
        "title": "Recursive CTE — Employee Hierarchy",
        "description": "Use a recursive CTE to show the full management chain for each employee (from root manager down to individual contributor).",
        "tables_used": ["employees"],
        "starter_sql": "WITH RECURSIVE hierarchy AS (\n  -- anchor: top-level managers\n  SELECT id, name, manager_id, 0 AS level, name AS path\n  FROM employees\n  WHERE manager_id IS NULL\n  UNION ALL\n  -- recursive: add direct reports\n  SELECT e.id, e.name, e.manager_id, h.level + 1,\n         h.path || ' > ' || e.name\n  FROM employees e\n  JOIN hierarchy h ON e.manager_id = h.id\n)\nSELECT * FROM hierarchy ORDER BY path;",
        "solution_sql": "WITH RECURSIVE hierarchy AS (\n    -- Anchor: top-level managers (no manager_id)\n    SELECT id,\n           name,\n           manager_id,\n           0          AS level,\n           name       AS path\n    FROM employees\n    WHERE manager_id IS NULL\n\n    UNION ALL\n\n    -- Recursive step: employees who report to someone in hierarchy\n    SELECT e.id,\n           e.name,\n           e.manager_id,\n           h.level + 1,\n           h.path || ' > ' || e.name\n    FROM employees e\n    INNER JOIN hierarchy h ON e.manager_id = h.id\n)\nSELECT level,\n       REPEAT('  ', level) || name AS indented_name,\n       path\nFROM hierarchy\nORDER BY path;",
        "explanation": """
<h3>Recursive CTE structure</h3>
<pre>WITH RECURSIVE cte AS (
  -- 1. Anchor member: starting rows (no self-reference)
  SELECT ... FROM table WHERE base_condition

  UNION ALL

  -- 2. Recursive member: references cte itself
  SELECT ... FROM table JOIN cte ON link_condition
)
SELECT * FROM cte;</pre>
<p>The engine runs the anchor once, then repeatedly runs the recursive member using the previous iteration's result until no new rows are produced.</p>
<h3>Common uses</h3>
<ul>
  <li>Org charts / management hierarchies</li>
  <li>Bill of materials (parts that contain parts)</li>
  <li>Graph traversal</li>
  <li>Generating number sequences</li>
</ul>
<p><strong>Caution:</strong> Recursive CTEs can loop infinitely on circular data. SQLite stops at a recursion depth limit.</p>
"""
    },


    # ─────────────────────────────────────────
    # INTERVIEW QUESTIONS
    # ─────────────────────────────────────────
    {
        "id": 54,
        "category": "Interview Questions",
        "title": "Nth Highest Salary",
        "description": "Find the <strong>3rd highest salary</strong> in the company. Your solution should work for any N — not just 3. Show at least 3 approaches.",
        "tables_used": ["employees"],
        "starter_sql": "-- Approach 1: Using OFFSET\nSELECT DISTINCT salary\nFROM employees\nORDER BY salary DESC\nLIMIT 1 OFFSET -- N-1 here;",
        "solution_sql": "-- Approach 1: LIMIT / OFFSET (simplest)\nSELECT DISTINCT salary AS third_highest\nFROM employees\nORDER BY salary DESC\nLIMIT 1 OFFSET 2;   -- OFFSET = N-1\n\n-- Approach 2: Subquery / NOT IN\nSELECT MAX(salary) AS third_highest\nFROM employees\nWHERE salary NOT IN (\n    SELECT DISTINCT salary\n    FROM employees\n    ORDER BY salary DESC\n    LIMIT 2            -- exclude top N-1 salaries\n);\n\n-- Approach 3: DENSE_RANK window function (best for ties)\nSELECT salary AS third_highest\nFROM (\n    SELECT DISTINCT salary,\n           DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk\n    FROM employees\n) ranked\nWHERE rnk = 3;",
        "explanation": """
<h3>The classic interview question</h3>
<p>Interviewers ask this because it tests multiple SQL skills at once: subqueries, window functions, handling ties, and NULL edge cases.</p>

<h3>Approach 1 — LIMIT / OFFSET</h3>
<pre>SELECT DISTINCT salary FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET 2;  -- 3rd highest → skip 2</pre>
<p>Simple and readable. DISTINCT ensures ties in the top positions don't consume an extra offset slot. Not supported by all databases (use <code>FETCH FIRST 1 ROW ONLY</code> in standard SQL).</p>

<h3>Approach 2 — NOT IN subquery</h3>
<pre>SELECT MAX(salary)
FROM employees
WHERE salary NOT IN (
    SELECT DISTINCT salary
    FROM employees
    ORDER BY salary DESC LIMIT 2
);</pre>
<p>Removes the top N-1 distinct salaries, then takes the MAX of what remains. Classic approach — works in older databases that lack window functions.</p>
<p><strong>Pitfall:</strong> If fewer than N distinct salaries exist, this returns NULL. Always handle that case.</p>

<h3>Approach 3 — DENSE_RANK (recommended)</h3>
<pre>SELECT salary FROM (
    SELECT DISTINCT salary,
           DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM employees
) t WHERE rnk = 3;</pre>
<p>Most robust. DENSE_RANK handles ties correctly — if two people share rank 1, rank 2 is the next distinct salary. Use this approach in interviews unless the interviewer forbids window functions.</p>

<h3>Handling NULL (what if N > number of distinct salaries?)</h3>
<pre>-- Wrap in COALESCE to return NULL gracefully:
SELECT COALESCE(
    (SELECT DISTINCT salary FROM employees ORDER BY salary DESC LIMIT 1 OFFSET 2),
    NULL
) AS third_highest;</pre>
"""
    },
    {
        "id": 55,
        "category": "Interview Questions",
        "title": "Find Duplicate Rows",
        "description": "Find all employee names that appear more than once in the <code>employees</code> table (duplicate names). Show the name and how many times it appears.",
        "tables_used": ["employees"],
        "starter_sql": "SELECT name, COUNT(*) AS occurrences\nFROM employees\nGROUP BY name\nHAVING -- condition for duplicates;",
        "solution_sql": "-- Method 1: GROUP BY + HAVING (most common)\nSELECT name,\n       COUNT(*) AS occurrences\nFROM employees\nGROUP BY name\nHAVING COUNT(*) > 1\nORDER BY occurrences DESC;\n\n-- Method 2: Self-join to show all duplicate rows\nSELECT DISTINCT e1.id, e1.name, e1.salary\nFROM employees e1\nINNER JOIN employees e2\n    ON e1.name = e2.name\n   AND e1.id  <> e2.id\nORDER BY e1.name;",
        "explanation": """
<h3>Method 1: GROUP BY + HAVING COUNT > 1</h3>
<p>The standard approach. Group by the column(s) that define "duplicate", then filter groups with more than one member.</p>
<pre>HAVING COUNT(*) > 1   -- appears 2+ times = duplicate</pre>
<p>This is also how you find duplicates on <em>combinations</em> of columns:</p>
<pre>GROUP BY first_name, last_name
HAVING COUNT(*) > 1</pre>

<h3>Method 2: Self-join</h3>
<p>To see the full rows (not just the duplicate values), self-join the table. The condition <code>e1.id &lt;&gt; e2.id</code> prevents a row from matching itself.</p>

<h3>Variation: duplicates across multiple columns</h3>
<pre>-- Find orders with duplicate (customer_id, product_id) pairs:
SELECT customer_id, product_id, COUNT(*) AS cnt
FROM orders
GROUP BY customer_id, product_id
HAVING COUNT(*) > 1;</pre>

<h3>Note on sample data</h3>
<p>The employees table in this sandbox has unique names, so this query returns no rows — but the technique is identical for any table with actual duplicates. Try it on the <code>orders</code> table to find customers who ordered the same product multiple times.</p>
"""
    },
    {
        "id": 56,
        "category": "Interview Questions",
        "title": "Employees Earning More Than Their Manager",
        "description": "Find all employees who earn a higher salary than their direct manager.",
        "tables_used": ["employees"],
        "starter_sql": "SELECT e.name AS employee, e.salary,\n       m.name AS manager, m.salary AS manager_salary\nFROM employees e\nJOIN employees m ON -- self join condition\nWHERE -- salary comparison;",
        "solution_sql": "SELECT e.name   AS employee,\n       e.salary AS employee_salary,\n       m.name   AS manager,\n       m.salary AS manager_salary,\n       e.salary - m.salary AS salary_difference\nFROM employees e\nINNER JOIN employees m ON e.manager_id = m.id\nWHERE e.salary > m.salary\nORDER BY salary_difference DESC;",
        "explanation": """
<h3>Self-join for hierarchical comparison</h3>
<p>This is a classic interview question testing self-joins. The key insight: the same table contains both employees AND managers — join it to itself.</p>
<pre>FROM employees e           -- "employee" copy
JOIN employees m           -- "manager" copy
  ON e.manager_id = m.id   -- link employee to their manager
WHERE e.salary > m.salary  -- filter: employee earns more</pre>

<h3>Why INNER JOIN?</h3>
<p>INNER JOIN excludes employees with <code>manager_id = NULL</code> (top-level managers like Alice Johnson). They have no manager to compare against, so they're correctly excluded.</p>
<p>If you wanted to explicitly include them in the output with a note:</p>
<pre>LEFT JOIN employees m ON e.manager_id = m.id
WHERE e.salary > COALESCE(m.salary, 0)  -- top-level: compare with 0</pre>

<h3>Common follow-up questions</h3>
<ul>
  <li>"Find employees earning more than the <em>average</em> salary of their department" — use a correlated subquery or window function <code>AVG(salary) OVER (PARTITION BY department_id)</code></li>
  <li>"Find managers whose entire team earns less than them" — requires GROUP BY + HAVING on the subordinates</li>
</ul>
"""
    },
    {
        "id": 57,
        "category": "Interview Questions",
        "title": "Second Highest Salary (Multiple Methods)",
        "description": "Find the second highest salary using at least 3 different approaches: subquery, DENSE_RANK, and a correlated subquery.",
        "tables_used": ["employees"],
        "starter_sql": "-- Try without LIMIT/OFFSET first (correlated subquery)\nSELECT MAX(salary)\nFROM employees\nWHERE salary < (SELECT MAX(salary) FROM employees);",
        "solution_sql": "-- Method 1: Exclude the MAX (classic, no window functions)\nSELECT MAX(salary) AS second_highest\nFROM employees\nWHERE salary < (SELECT MAX(salary) FROM employees);\n\n-- Method 2: DENSE_RANK\nSELECT salary AS second_highest\nFROM (\n    SELECT salary,\n           DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk\n    FROM employees\n) t\nWHERE rnk = 2\nLIMIT 1;\n\n-- Method 3: LIMIT / OFFSET\nSELECT DISTINCT salary AS second_highest\nFROM employees\nORDER BY salary DESC\nLIMIT 1 OFFSET 1;\n\n-- Method 4: Correlated subquery (count how many salaries are greater)\nSELECT DISTINCT salary AS second_highest\nFROM employees e1\nWHERE 1 = (\n    SELECT COUNT(DISTINCT salary)\n    FROM employees e2\n    WHERE e2.salary > e1.salary\n)\nLIMIT 1;",
        "explanation": """
<h3>Method 1: Subquery to exclude the max</h3>
<pre>SELECT MAX(salary) FROM employees
WHERE salary &lt; (SELECT MAX(salary) FROM employees)</pre>
<p>Elegant and widely understood. Works in all databases. But breaks for the "Nth highest" — you'd have to nest N-1 subqueries.</p>

<h3>Method 2: DENSE_RANK (most scalable)</h3>
<p>Generalizes perfectly to "Nth highest" — just change <code>rnk = 2</code> to <code>rnk = N</code>.</p>

<h3>Method 3: LIMIT / OFFSET</h3>
<pre>LIMIT 1 OFFSET 1  -- skip rank 1, take rank 2</pre>
<p>Clean and fast, but requires DISTINCT to handle tied top salaries correctly.</p>

<h3>Method 4: Correlated subquery (without window functions or LIMIT)</h3>
<pre>WHERE 1 = (SELECT COUNT(DISTINCT salary)
            FROM employees e2
            WHERE e2.salary > e1.salary)</pre>
<p>For the 2nd highest, exactly 1 distinct salary is higher. For Nth highest, change <code>1</code> to <code>N-1</code>. This works in all SQL dialects including old MySQL versions — useful to know even though it's slower.</p>

<h3>Interviewer tip</h3>
<p>When asked this question, always ask: "Should I handle ties? If two employees share the highest salary, should I return NULL or the next distinct salary?" The answer determines whether you use DISTINCT and DENSE_RANK vs ROW_NUMBER.</p>
"""
    },
    {
        "id": 58,
        "category": "Interview Questions",
        "title": "Department with Highest Average Salary",
        "description": "Find the department (show its name) that has the highest average employee salary.",
        "tables_used": ["employees", "departments"],
        "starter_sql": "SELECT d.name, ROUND(AVG(e.salary), 2) AS avg_salary\nFROM employees e\nJOIN departments d ON e.department_id = d.id\nGROUP BY d.id, d.name\n-- filter to just the top one;",
        "solution_sql": "-- Method 1: ORDER BY + LIMIT\nSELECT d.name               AS department,\n       ROUND(AVG(e.salary), 2) AS avg_salary\nFROM employees e\nINNER JOIN departments d ON e.department_id = d.id\nGROUP BY d.id, d.name\nORDER BY avg_salary DESC\nLIMIT 1;\n\n-- Method 2: Subquery (works if you want all tied departments)\nSELECT d.name               AS department,\n       ROUND(AVG(e.salary), 2) AS avg_salary\nFROM employees e\nINNER JOIN departments d ON e.department_id = d.id\nGROUP BY d.id, d.name\nHAVING AVG(e.salary) = (\n    SELECT MAX(dept_avg)\n    FROM (\n        SELECT AVG(salary) AS dept_avg\n        FROM employees\n        GROUP BY department_id\n    )\n);",
        "explanation": """
<h3>Method 1: ORDER BY + LIMIT 1</h3>
<p>The simplest approach. Calculate average per department, sort descending, take the top row.</p>
<p><strong>Limitation:</strong> If two departments tie for the highest average, LIMIT 1 arbitrarily returns one of them.</p>

<h3>Method 2: Subquery in HAVING (handles ties)</h3>
<p>The inner subquery calculates the max of all department averages. The outer query's HAVING clause then keeps only departments whose average equals that maximum.</p>
<p>This correctly returns <em>all</em> tied departments.</p>

<h3>Method 3: Using RANK (most complete)</h3>
<pre>WITH dept_avgs AS (
    SELECT d.name, AVG(e.salary) AS avg_sal
    FROM employees e JOIN departments d ON e.department_id = d.id
    GROUP BY d.id, d.name
)
SELECT name, ROUND(avg_sal, 2) AS avg_salary
FROM dept_avgs
WHERE avg_sal = (SELECT MAX(avg_sal) FROM dept_avgs);</pre>
"""
    },
    {
        "id": 59,
        "category": "Interview Questions",
        "title": "Find Gaps in a Sequence",
        "description": "Find any missing IDs (gaps) in the <code>orders</code> table. The IDs should be consecutive from 1 to the maximum. Show the missing values.",
        "tables_used": ["orders"],
        "starter_sql": "-- Use a recursive CTE to generate a full sequence\n-- then LEFT JOIN with orders to find gaps\nWITH RECURSIVE seq(n) AS (\n  SELECT 1\n  UNION ALL\n  SELECT n + 1 FROM seq WHERE n < (SELECT MAX(id) FROM orders)\n)\nSELECT seq.n AS missing_id\nFROM seq\nLEFT JOIN orders o ON seq.n = o.id\nWHERE o.id IS NULL;",
        "solution_sql": "-- Generate full sequence 1..MAX(id) then find gaps\nWITH RECURSIVE seq(n) AS (\n    SELECT 1\n    UNION ALL\n    SELECT n + 1 FROM seq\n    WHERE n < (SELECT MAX(id) FROM orders)\n)\nSELECT seq.n AS missing_id\nFROM seq\nLEFT JOIN orders o ON seq.n = o.id\nWHERE o.id IS NULL\nORDER BY missing_id;\n\n-- Alternative: LAG to detect jumps in existing data\nSELECT prev_id + 1   AS gap_start,\n       curr_id - 1   AS gap_end,\n       curr_id - prev_id - 1 AS missing_count\nFROM (\n    SELECT id AS curr_id,\n           LAG(id) OVER (ORDER BY id) AS prev_id\n    FROM orders\n) t\nWHERE curr_id - prev_id > 1;",
        "explanation": """
<h3>Method 1: Recursive CTE + LEFT JOIN</h3>
<p>Generate a complete sequence from 1 to MAX(id) using a recursive CTE, then LEFT JOIN with the actual table. Rows where the join fails (o.id IS NULL) are the gaps.</p>
<pre>WITH RECURSIVE seq(n) AS (
    SELECT 1                              -- anchor
    UNION ALL
    SELECT n + 1 FROM seq WHERE n &lt; max  -- recursive step
)
SELECT n FROM seq LEFT JOIN orders ON seq.n = orders.id
WHERE orders.id IS NULL;</pre>

<h3>Method 2: LAG to detect jumps</h3>
<p>More efficient for large tables — only scans the existing rows rather than generating every integer. LAG gives the previous ID; if the jump is more than 1, there's a gap.</p>
<pre>curr_id - prev_id &gt; 1  →  there's a gap between them</pre>
<p>This also tells you the <em>range</em> of missing IDs (gap_start to gap_end), not just that a gap exists.</p>

<h3>Note on the sample data</h3>
<p>The orders table in this sandbox has consecutive IDs 1–25 with no gaps. To test, try on a table where you know IDs are missing, or add a filter like <code>WHERE id NOT IN (5, 10, 15)</code> in a subquery.</p>
"""
    },
    {
        "id": 60,
        "category": "Interview Questions",
        "title": "Cumulative / Running Percentage",
        "description": "Show each employee's salary, their running total salary (cumulative sum ordered by salary descending), and what percentage of the total salary budget they represent cumulatively.",
        "tables_used": ["employees"],
        "starter_sql": "SELECT name, salary,\n  SUM(salary) OVER (ORDER BY salary DESC\n    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total,\n  -- add cumulative percentage\nFROM employees\nORDER BY salary DESC;",
        "solution_sql": "SELECT name,\n       salary,\n       SUM(salary) OVER (\n           ORDER BY salary DESC\n           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW\n       )                                        AS running_total,\n       ROUND(\n           100.0 * SUM(salary) OVER (\n               ORDER BY salary DESC\n               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW\n           ) / SUM(salary) OVER (),\n       1)                                       AS cumulative_pct,\n       ROUND(100.0 * salary / SUM(salary) OVER(), 2) AS pct_of_total\nFROM employees\nORDER BY salary DESC;",
        "explanation": """
<h3>Two window functions in one query</h3>
<p>This question combines:</p>
<ol>
  <li><strong>Running total:</strong> <code>SUM(salary) OVER (ORDER BY salary DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)</code></li>
  <li><strong>Grand total:</strong> <code>SUM(salary) OVER ()</code> — no PARTITION BY or ORDER BY means the entire result is one partition, so this returns the same grand total for every row</li>
  <li><strong>Cumulative %:</strong> running_total / grand_total × 100</li>
</ol>

<h3>SUM() OVER () — the grand total trick</h3>
<pre>SUM(salary) OVER ()  -- grand total, same for every row</pre>
<p>An empty OVER() clause means no partitioning and no ordering — the window is the entire result set. This is a very common pattern for computing row-level percentages of a total.</p>

<h3>Practical use</h3>
<p>This kind of query is used in Pareto analysis — e.g., "the top 20% of employees represent what percentage of the total salary budget?" You'd filter <code>WHERE cumulative_pct &lt;= 80</code> to find the employees that make up the first 80% of the salary bill.</p>
"""
    },
    {
        "id": 61,
        "category": "Interview Questions",
        "title": "Consecutive Days / Streak Detection",
        "description": "For each employee in the <code>sales</code> table, find the longest streak of consecutive months in which they made at least one sale.",
        "tables_used": ["sales"],
        "starter_sql": "-- Step 1: get distinct year-month per employee\n-- Step 2: use ROW_NUMBER - a date sequence to detect gaps\nWITH months AS (\n  SELECT DISTINCT employee_id,\n         STRFTIME('%Y-%m', sale_date) AS ym\n  FROM sales\n)\nSELECT * FROM months ORDER BY employee_id, ym;",
        "solution_sql": "WITH months AS (\n    -- distinct months per employee\n    SELECT DISTINCT\n           employee_id,\n           STRFTIME('%Y-%m', sale_date) AS ym,\n           -- convert YYYY-MM to a numeric month index for arithmetic\n           CAST(STRFTIME('%Y', sale_date) AS INT) * 12\n           + CAST(STRFTIME('%m', sale_date) AS INT) AS month_num\n    FROM sales\n),\ngrp AS (\n    -- Subtract ROW_NUMBER from month_num.\n    -- Rows in the same consecutive run share the same (month_num - row_number) value.\n    SELECT employee_id,\n           ym,\n           month_num,\n           month_num - ROW_NUMBER() OVER (\n               PARTITION BY employee_id\n               ORDER BY month_num\n           ) AS streak_group\n    FROM months\n)\nSELECT employee_id,\n       MIN(ym)        AS streak_start,\n       MAX(ym)        AS streak_end,\n       COUNT(*)       AS streak_length\nFROM grp\nGROUP BY employee_id, streak_group\nORDER BY streak_length DESC, employee_id;",
        "explanation": """
<h3>The "gaps and islands" pattern</h3>
<p>This is one of the most elegant SQL patterns. The trick: subtract a sequential row number from a sequential date value. For consecutive values, this difference is constant. For a gap, the difference changes — starting a new "island".</p>
<pre>month_num:   24277  24278  24279   ←  consecutive (+1 each)
row_num:         1      2      3   ←  consecutive (+1 each)
difference:  24276  24276  24276   ←  SAME → same streak group

month_num:   24277  24278  24280   ←  gap after 24279
row_num:         1      2      3
difference:  24276  24276  24277   ←  DIFFERENT → new streak</pre>

<h3>Why month_num arithmetic?</h3>
<p><code>year * 12 + month</code> converts 'YYYY-MM' into a linear integer. Consecutive months differ by 1, which is what the subtraction trick requires.</p>

<h3>Common variations</h3>
<ul>
  <li>Longest streak of login days for a user</li>
  <li>Consecutive winning days in trading (price went up)</li>
  <li>Consecutive quarters with revenue growth</li>
</ul>
<p>The pattern is always the same: convert to a number, subtract ROW_NUMBER, group by the constant difference.</p>
"""
    },
    {
        "id": 62,
        "category": "Interview Questions",
        "title": "Pivot — Sales by Region per Employee",
        "description": "Create a pivot table showing each salesperson's total sales broken down by region (North, South, East, West) — each region as a separate column.",
        "tables_used": ["sales", "employees"],
        "starter_sql": "SELECT e.name,\n  SUM(CASE WHEN s.region = 'North' THEN s.amount ELSE 0 END) AS North,\n  -- add South, East, West\nFROM sales s\nJOIN employees e ON s.employee_id = e.id\nGROUP BY e.id, e.name;",
        "solution_sql": "SELECT e.name                                                    AS employee,\n       SUM(CASE WHEN s.region = 'North' THEN s.amount ELSE 0 END) AS North,\n       SUM(CASE WHEN s.region = 'South' THEN s.amount ELSE 0 END) AS South,\n       SUM(CASE WHEN s.region = 'East'  THEN s.amount ELSE 0 END) AS East,\n       SUM(CASE WHEN s.region = 'West'  THEN s.amount ELSE 0 END) AS West,\n       SUM(s.amount)                                               AS Total\nFROM sales s\nINNER JOIN employees e ON s.employee_id = e.id\nGROUP BY e.id, e.name\nORDER BY Total DESC;",
        "explanation": """
<h3>Manual PIVOT with conditional aggregation</h3>
<p>SQL doesn't have a universal PIVOT syntax (Oracle and SQL Server do, but not MySQL or SQLite). The standard approach is <strong>conditional aggregation</strong>: use CASE WHEN inside SUM to conditionally add to a column.</p>
<pre>SUM(CASE WHEN region = 'North' THEN amount ELSE 0 END) AS North</pre>
<p>This reads: "For each row in the group, if the region is North, add the amount to the running sum; otherwise add 0."</p>

<h3>Equivalent in databases with PIVOT syntax (SQL Server)</h3>
<pre>SELECT * FROM sales
PIVOT (
    SUM(amount)
    FOR region IN ([North], [South], [East], [West])
) AS pvt;</pre>

<h3>Common interview follow-up</h3>
<p>"What if you don't know the list of regions in advance?" — In that case you need dynamic SQL (building and executing a query string at runtime), which is database-specific and generally outside standard SQL.</p>

<h3>Un-pivoting (UNPIVOT)</h3>
<p>The reverse operation (wide → tall) uses UNION ALL:</p>
<pre>SELECT employee, 'North' AS region, North AS amount FROM pivot_table
UNION ALL
SELECT employee, 'South', South FROM pivot_table
...</pre>
"""
    },
    {
        "id": 63,
        "category": "Interview Questions",
        "title": "Customers Who Placed Orders in Every Month",
        "description": "Find customers who placed at least one order in <em>every month</em> that exists in the orders table (i.e., they were consistently active every month).",
        "tables_used": ["orders", "customers"],
        "starter_sql": "-- Step 1: count total distinct months in orders table\n-- Step 2: count distinct months each customer ordered in\n-- Step 3: find customers where both counts match\nWITH total_months AS (\n  SELECT COUNT(DISTINCT STRFTIME('%Y-%m', order_date)) AS cnt\n  FROM orders\n)\nSELECT customer_id, COUNT(DISTINCT STRFTIME('%Y-%m', order_date)) AS active_months\nFROM orders\nGROUP BY customer_id\nHAVING active_months = (SELECT cnt FROM total_months);",
        "solution_sql": "WITH total_months AS (\n    SELECT COUNT(DISTINCT STRFTIME('%Y-%m', order_date)) AS cnt\n    FROM orders\n),\ncustomer_months AS (\n    SELECT customer_id,\n           COUNT(DISTINCT STRFTIME('%Y-%m', order_date)) AS active_months\n    FROM orders\n    GROUP BY customer_id\n)\nSELECT c.name,\n       cm.active_months,\n       tm.cnt AS total_months\nFROM customer_months cm\nINNER JOIN total_months tm ON cm.active_months = tm.cnt\nINNER JOIN customers c    ON cm.customer_id  = c.id\nORDER BY c.name;",
        "explanation": """
<h3>Relational division</h3>
<p>This is an instance of <strong>relational division</strong> — "find X such that X is related to ALL Y." Classic examples:</p>
<ul>
  <li>Customers who ordered every product</li>
  <li>Students who attended every class</li>
  <li>Employees who worked every shift</li>
</ul>

<h3>The counting trick</h3>
<p>The simplest approach: a customer ordered in "every month" if the number of distinct months they ordered in equals the total number of distinct months in the dataset.</p>
<pre>customer_active_months = total_distinct_months</pre>

<h3>Limitations</h3>
<p>This approach assumes "every month" means every month that <em>appears in the orders table</em>. If you want "every calendar month in a date range", generate the full calendar first with a recursive CTE.</p>

<h3>Alternative: NOT EXISTS (relational division)</h3>
<pre>SELECT c.id FROM customers c
WHERE NOT EXISTS (
    SELECT DISTINCT STRFTIME('%Y-%m', order_date) AS m FROM orders
    EXCEPT
    SELECT DISTINCT STRFTIME('%Y-%m', order_date) FROM orders WHERE customer_id = c.id
);</pre>
<p>"There is no month where the customer did NOT order" — logically equivalent, but more complex.</p>
"""
    },
    {
        "id": 64,
        "category": "Interview Questions",
        "title": "Moving Average",
        "description": "Calculate a 3-period moving average of total order revenue. For each month, show the month, total revenue, and the average of the current month + the 2 preceding months.",
        "tables_used": ["orders"],
        "starter_sql": "WITH monthly AS (\n  SELECT STRFTIME('%Y-%m', order_date) AS month,\n         SUM(total_amount) AS revenue\n  FROM orders GROUP BY month\n)\nSELECT month, revenue,\n  AVG(revenue) OVER (\n    ORDER BY month\n    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW\n  ) AS moving_avg_3\nFROM monthly ORDER BY month;",
        "solution_sql": "WITH monthly AS (\n    SELECT STRFTIME('%Y-%m', order_date) AS month,\n           SUM(total_amount)            AS revenue\n    FROM orders\n    GROUP BY STRFTIME('%Y-%m', order_date)\n)\nSELECT month,\n       ROUND(revenue, 2)    AS revenue,\n       ROUND(AVG(revenue) OVER (\n           ORDER BY month\n           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW\n       ), 2)                AS moving_avg_3m,\n       COUNT(*) OVER (\n           ORDER BY month\n           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW\n       )                    AS periods_in_avg\nFROM monthly\nORDER BY month;",
        "explanation": """
<h3>Window frame for moving averages</h3>
<pre>AVG(revenue) OVER (
    ORDER BY month
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
)</pre>
<p>The frame <code>2 PRECEDING AND CURRENT ROW</code> includes the current row plus the 2 rows before it — a 3-row window that slides forward with each row.</p>

<h3>ROWS vs RANGE</h3>
<p>Use <code>ROWS</code> for moving averages to avoid surprises when multiple rows share the same ORDER BY value. <code>RANGE</code> would include all rows with the same month value in the window, potentially expanding the frame unexpectedly.</p>

<h3>The periods_in_avg column</h3>
<p>The first two months only have 1 and 2 periods available (you can't look back before the first row). Adding <code>COUNT(*) OVER (...)</code> with the same frame shows how many periods were actually averaged — useful for knowing when the moving average is "warm" (has enough history).</p>

<h3>Common variations</h3>
<ul>
  <li>7-day moving average: <code>ROWS BETWEEN 6 PRECEDING AND CURRENT ROW</code></li>
  <li>Centered moving average (3-period): <code>ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING</code></li>
  <li>Exponential moving average: requires a recursive CTE (more complex)</li>
</ul>
"""
    },
    {
        "id": 65,
        "category": "Interview Questions",
        "title": "Top Customers by Spending (with Ties)",
        "description": "Find the top 3 customers by total spending. If customers tie for 3rd place, include ALL of them (don't arbitrarily cut ties with LIMIT).",
        "tables_used": ["orders", "customers"],
        "starter_sql": "-- LIMIT 3 alone won't handle ties correctly.\n-- Use DENSE_RANK to properly include all tied 3rd-place customers.\nWITH ranked AS (\n  SELECT customer_id, SUM(total_amount) AS total_spent,\n         DENSE_RANK() OVER (ORDER BY SUM(total_amount) DESC) AS rnk\n  FROM orders GROUP BY customer_id\n)\nSELECT -- join with customers and filter rnk <= 3;",
        "solution_sql": "WITH customer_totals AS (\n    SELECT customer_id,\n           SUM(total_amount) AS total_spent\n    FROM orders\n    GROUP BY customer_id\n),\nranked AS (\n    SELECT customer_id,\n           total_spent,\n           DENSE_RANK() OVER (ORDER BY total_spent DESC) AS spending_rank\n    FROM customer_totals\n)\nSELECT c.name,\n       ROUND(r.total_spent, 2)  AS total_spent,\n       r.spending_rank\nFROM ranked r\nINNER JOIN customers c ON r.customer_id = c.id\nWHERE r.spending_rank <= 3\nORDER BY r.spending_rank, c.name;",
        "explanation": """
<h3>The tie-handling problem</h3>
<p>Using <code>ORDER BY total DESC LIMIT 3</code> can silently exclude customers who share the 3rd-place spending amount. This is wrong for business reporting.</p>

<h3>DENSE_RANK for tie-safe Top-N</h3>
<pre>DENSE_RANK() OVER (ORDER BY total_spent DESC) = 3rd rank</pre>
<p>DENSE_RANK assigns the same rank to ties and doesn't skip numbers. <code>WHERE rank &lt;= 3</code> returns all customers in the top 3 <em>tiers</em>, regardless of how many customers share a tier.</p>

<h3>RANK vs DENSE_RANK for Top-N</h3>
<ul>
  <li><code>RANK() &lt;= 3</code> — includes customers ranked 1, 2, 3. But if two customers tie for rank 1, rank 3 is skipped (becomes rank 4), so you might get 3 customers total — not the "top 3 tiers".</li>
  <li><code>DENSE_RANK() &lt;= 3</code> — always returns customers in the top 3 distinct spending levels. Recommended for "top N" problems.</li>
</ul>

<h3>Follow-up: What if the interviewer says "exactly 3 rows, break ties randomly"?</h3>
<pre>SELECT c.name, SUM(o.total_amount) AS total_spent
FROM orders o JOIN customers c ON o.customer_id = c.id
GROUP BY c.id, c.name
ORDER BY total_spent DESC
LIMIT 3;  -- arbitrary tie-breaking, but deterministic with a stable sort</pre>
"""
    },
    {
        "id": 66,
        "category": "Interview Questions",
        "title": "Products Never Ordered",
        "description": "Find all products that have never been ordered. Use three different approaches: LEFT JOIN, NOT IN, and NOT EXISTS.",
        "tables_used": ["products", "orders"],
        "starter_sql": "-- Method 1: LEFT JOIN + IS NULL\nSELECT p.name\nFROM products p\nLEFT JOIN orders o ON p.id = o.product_id\nWHERE o.product_id IS NULL;",
        "solution_sql": "-- Method 1: LEFT JOIN + IS NULL (most common)\nSELECT p.name, p.category, p.price\nFROM products p\nLEFT JOIN orders o ON p.id = o.product_id\nWHERE o.product_id IS NULL\nORDER BY p.name;\n\n-- Method 2: NOT IN\nSELECT name, category, price\nFROM products\nWHERE id NOT IN (\n    SELECT DISTINCT product_id FROM orders\n)\nORDER BY name;\n\n-- Method 3: NOT EXISTS (safest with NULLs)\nSELECT p.name, p.category, p.price\nFROM products p\nWHERE NOT EXISTS (\n    SELECT 1 FROM orders o WHERE o.product_id = p.id\n)\nORDER BY p.name;",
        "explanation": """
<h3>Three equivalent approaches</h3>

<h4>Method 1: LEFT JOIN + IS NULL</h4>
<p>Arguably the most readable. A LEFT JOIN keeps all products; where no order matches, the orders columns are NULL. Filter <code>WHERE o.product_id IS NULL</code> to get unordered products.</p>

<h4>Method 2: NOT IN</h4>
<p>Simple but has a dangerous gotcha: if the subquery returns any NULL, <code>NOT IN</code> returns NO rows (because <code>x NOT IN (1, 2, NULL)</code> evaluates to UNKNOWN for all x). Safe here since <code>product_id</code> is NOT NULL in orders, but risky in general.</p>

<h4>Method 3: NOT EXISTS (recommended)</h4>
<p>Null-safe, short-circuits on first match, often well-optimized. The idiom <code>SELECT 1</code> inside EXISTS is a convention — only the existence of a row matters, not its value.</p>

<h3>Performance comparison</h3>
<table>
  <tr><th>Method</th><th>NULL-safe?</th><th>Short-circuits?</th><th>Notes</th></tr>
  <tr><td>LEFT JOIN + IS NULL</td><td>Yes</td><td>No</td><td>Good for selecting other columns from the joined table</td></tr>
  <tr><td>NOT IN</td><td>No ⚠️</td><td>No</td><td>Avoid when subquery might return NULLs</td></tr>
  <tr><td>NOT EXISTS</td><td>Yes</td><td>Yes</td><td>Usually fastest; preferred in most cases</td></tr>
</table>
"""
    },
    {
        "id": 67,
        "category": "Interview Questions",
        "title": "Median Salary",
        "description": "Calculate the median salary of all employees. SQLite has no built-in MEDIAN function — implement it using window functions.",
        "tables_used": ["employees"],
        "starter_sql": "-- Find the middle value(s) using ROW_NUMBER and COUNT\nWITH ordered AS (\n  SELECT salary,\n         ROW_NUMBER() OVER (ORDER BY salary) AS rn,\n         COUNT(*) OVER () AS total\n  FROM employees\n)\nSELECT AVG(salary) AS median_salary\nFROM ordered\nWHERE rn IN ((total + 1) / 2, (total + 2) / 2);",
        "solution_sql": "-- Method 1: Row-numbering (works for odd and even counts)\nWITH ordered AS (\n    SELECT salary,\n           ROW_NUMBER() OVER (ORDER BY salary)       AS rn,\n           COUNT(*)     OVER ()                       AS total\n    FROM employees\n)\nSELECT ROUND(AVG(salary), 2) AS median_salary\nFROM ordered\nWHERE rn IN (\n    (total + 1) / 2,    -- middle for odd count, lower-middle for even\n    (total + 2) / 2     -- same as above for odd; upper-middle for even\n);\n\n-- Method 2: PERCENTILE_CONT (standard SQL, not supported in SQLite)\n-- SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median\n-- FROM employees;",
        "explanation": """
<h3>Why median is tricky in SQL</h3>
<p>The median is the middle value when sorted. For an odd count (e.g., 5 values), it's the 3rd. For an even count (e.g., 6 values), it's the average of the 3rd and 4th.</p>

<h3>The ROW_NUMBER approach</h3>
<pre>WHERE rn IN ((total + 1) / 2, (total + 2) / 2)</pre>
<p>Integer arithmetic:</p>
<ul>
  <li>20 employees: <code>(20+1)/2 = 10</code>, <code>(20+2)/2 = 11</code> → average of rows 10 and 11 (even count)</li>
  <li>19 employees: <code>(19+1)/2 = 10</code>, <code>(19+2)/2 = 10</code> → row 10 only (odd count)</li>
</ul>
<p>Taking AVG of the selected rows handles both cases: for odd counts, AVG of a single value is that value itself.</p>

<h3>Built-in support</h3>
<ul>
  <li><strong>PostgreSQL:</strong> <code>PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary)</code></li>
  <li><strong>MySQL 8+:</strong> Same as PostgreSQL</li>
  <li><strong>SQLite:</strong> No built-in; use the window function approach above</li>
</ul>
"""
    },
    {
        "id": 68,
        "category": "Interview Questions",
        "title": "Employees with Salary Above Department Average",
        "description": "List every employee whose salary is above their own department's average salary. Show the employee, their salary, the department average, and the difference.",
        "tables_used": ["employees"],
        "starter_sql": "-- Use a window function for the cleanest solution\nSELECT name, salary, department_id,\n  ROUND(AVG(salary) OVER (PARTITION BY department_id), 2) AS dept_avg\nFROM employees\nWHERE salary > -- department avg;",
        "solution_sql": "-- Method 1: Window function (cleanest, single table scan)\nWITH dept_context AS (\n    SELECT name,\n           salary,\n           department_id,\n           ROUND(AVG(salary) OVER (PARTITION BY department_id), 2) AS dept_avg\n    FROM employees\n)\nSELECT name,\n       salary,\n       department_id,\n       dept_avg,\n       ROUND(salary - dept_avg, 2) AS above_avg_by\nFROM dept_context\nWHERE salary > dept_avg\nORDER BY department_id, above_avg_by DESC;\n\n-- Method 2: Correlated subquery (classic approach)\nSELECT name, salary, department_id,\n       ROUND((SELECT AVG(salary) FROM employees e2\n              WHERE e2.department_id = e1.department_id), 2) AS dept_avg\nFROM employees e1\nWHERE salary > (SELECT AVG(salary) FROM employees e2\n                WHERE e2.department_id = e1.department_id)\nORDER BY department_id, salary DESC;",
        "explanation": """
<h3>Why you can't filter on a window function directly</h3>
<p>This doesn't work:</p>
<pre>-- WRONG:
SELECT name, salary, AVG(salary) OVER (PARTITION BY department_id) AS dept_avg
FROM employees
WHERE salary > dept_avg;  -- ERROR: dept_avg doesn't exist yet in WHERE</pre>
<p>Window functions are evaluated <em>after</em> WHERE, so the alias doesn't exist when WHERE is processed. You must wrap in a CTE or subquery.</p>

<h3>Method 1: Window function + CTE (recommended)</h3>
<p>Single pass over the table. The CTE computes <code>dept_avg</code> for every row, then the outer query filters and shows results. Very efficient — the optimizer often does just one table scan.</p>

<h3>Method 2: Correlated subquery (classic)</h3>
<p>For each employee, the subquery recalculates the department average. Executed once per row — O(n²) in theory but optimized by modern databases. Easier to understand but less efficient at large scale.</p>

<h3>Method 3: JOIN with aggregated subquery</h3>
<pre>SELECT e.name, e.salary, d.dept_avg
FROM employees e
JOIN (SELECT department_id, AVG(salary) AS dept_avg
      FROM employees GROUP BY department_id) d
  ON e.department_id = d.department_id
WHERE e.salary > d.dept_avg;</pre>
"""
    },
    {
        "id": 69,
        "category": "Interview Questions",
        "title": "Find Managers with All Reports Below Median",
        "description": "Find managers where <em>every single one</em> of their direct reports earns less than the company-wide median salary.",
        "tables_used": ["employees"],
        "starter_sql": "-- Step 1: Compute median\n-- Step 2: Find managers whose MAX subordinate salary < median\nWITH median_cte AS (\n  -- median salary\n  SELECT AVG(salary) AS median_salary\n  FROM (\n    SELECT salary, ROW_NUMBER() OVER (ORDER BY salary) rn, COUNT(*) OVER() tot\n    FROM employees\n  ) t WHERE rn IN ((tot+1)/2, (tot+2)/2)\n)\nSELECT -- find qualifying managers;",
        "solution_sql": "WITH median_cte AS (\n    SELECT AVG(salary) AS median_salary\n    FROM (\n        SELECT salary,\n               ROW_NUMBER() OVER (ORDER BY salary) AS rn,\n               COUNT(*) OVER ()                    AS tot\n        FROM employees\n    ) t\n    WHERE rn IN ((tot + 1) / 2, (tot + 2) / 2)\n),\nmanager_report_max AS (\n    SELECT m.id          AS manager_id,\n           m.name        AS manager_name,\n           m.salary      AS manager_salary,\n           MAX(e.salary) AS max_report_salary,\n           COUNT(e.id)   AS num_reports\n    FROM employees m\n    INNER JOIN employees e ON e.manager_id = m.id\n    GROUP BY m.id, m.name, m.salary\n)\nSELECT mrm.manager_name,\n       mrm.manager_salary,\n       mrm.num_reports,\n       mrm.max_report_salary,\n       ROUND(mc.median_salary, 2) AS company_median\nFROM manager_report_max mrm\nCROSS JOIN median_cte mc\nWHERE mrm.max_report_salary < mc.median_salary\nORDER BY mrm.num_reports DESC;",
        "explanation": """
<h3>Breaking this down into steps</h3>
<ol>
  <li><strong>median_cte</strong> — compute the company median (see Question #67 for the technique)</li>
  <li><strong>manager_report_max</strong> — for each manager, get the max salary among all their direct reports and the count of reports</li>
  <li><strong>Main query</strong> — join with CROSS JOIN (since there's only one median row) and filter managers where their highest-paid report is still below the median</li>
</ol>

<h3>CROSS JOIN with a scalar CTE</h3>
<p>When one table in a join has exactly one row, a CROSS JOIN is safe and clean — it simply attaches that single row's values to every row of the other table. This is a common pattern for joining a "scalar" result (like a company-wide statistic) to a row-level result.</p>

<h3>The logic</h3>
<p>"Every single report earns less than median" is equivalent to "the MAX report salary &lt; median". If even the highest-paid report is below median, all reports are below median.</p>
<p>This is a powerful technique: use aggregate functions (MAX, MIN, ALL) to check a condition across a group without needing correlated subqueries for each row.</p>
"""
    },
]

CATEGORIES = list(dict.fromkeys(q["category"] for q in QUESTIONS))
