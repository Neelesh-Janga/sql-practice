def seed_database(conn):
    """Create all tables and insert sample data into the given SQLite connection."""
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS departments (
            id          INTEGER PRIMARY KEY,
            name        TEXT NOT NULL,
            location    TEXT NOT NULL,
            budget      REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS employees (
            id            INTEGER PRIMARY KEY,
            name          TEXT NOT NULL,
            department_id INTEGER REFERENCES departments(id),
            salary        REAL NOT NULL,
            hire_date     TEXT NOT NULL,
            manager_id    INTEGER REFERENCES employees(id),
            gender        TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS customers (
            id           INTEGER PRIMARY KEY,
            name         TEXT NOT NULL,
            email        TEXT NOT NULL,
            city         TEXT NOT NULL,
            country      TEXT NOT NULL,
            signup_date  TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS products (
            id        INTEGER PRIMARY KEY,
            name      TEXT NOT NULL,
            category  TEXT NOT NULL,
            price     REAL NOT NULL,
            stock     INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS orders (
            id            INTEGER PRIMARY KEY,
            customer_id   INTEGER REFERENCES customers(id),
            product_id    INTEGER REFERENCES products(id),
            quantity      INTEGER NOT NULL,
            order_date    TEXT NOT NULL,
            status        TEXT NOT NULL,
            total_amount  REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS sales (
            id          INTEGER PRIMARY KEY,
            employee_id INTEGER REFERENCES employees(id),
            amount      REAL NOT NULL,
            sale_date   TEXT NOT NULL,
            region      TEXT NOT NULL
        );
    """)

    cur.executemany(
        "INSERT INTO departments (id, name, location, budget) VALUES (?, ?, ?, ?)",
        [
            (1,  'Engineering',  'New York',      1200000),
            (2,  'Marketing',    'San Francisco', 800000),
            (3,  'Sales',        'Chicago',       950000),
            (4,  'HR',           'Austin',        400000),
            (5,  'Finance',      'New York',      600000),
            (6,  'Operations',   'Seattle',       750000),
        ]
    )

    cur.executemany(
        "INSERT INTO employees (id, name, department_id, salary, hire_date, manager_id, gender) VALUES (?, ?, ?, ?, ?, ?, ?)",
        [
            (1,  'Alice Johnson',    1, 95000,  '2018-03-15', None, 'F'),
            (2,  'Bob Smith',        1, 82000,  '2019-07-22', 1,    'M'),
            (3,  'Carol White',      2, 76000,  '2020-01-10', None, 'F'),
            (4,  'David Brown',      3, 68000,  '2017-11-05', None, 'M'),
            (5,  'Eva Martinez',     1, 91000,  '2018-06-30', 1,    'F'),
            (6,  'Frank Lee',        4, 58000,  '2021-02-14', None, 'M'),
            (7,  'Grace Kim',        2, 72000,  '2019-09-01', 3,    'F'),
            (8,  'Henry Wilson',     3, 64000,  '2020-04-18', 4,    'M'),
            (9,  'Iris Chen',        5, 88000,  '2016-12-03', None, 'F'),
            (10, 'James Davis',      1, 78000,  '2021-08-25', 1,    'M'),
            (11, 'Karen Taylor',     6, 61000,  '2022-01-11', None, 'F'),
            (12, 'Leo Anderson',     3, 70000,  '2018-05-07', 4,    'M'),
            (13, 'Mia Thomas',       2, 79000,  '2020-10-20', 3,    'F'),
            (14, 'Nathan Harris',    5, 93000,  '2015-09-14', 9,    'M'),
            (15, 'Olivia Clark',     4, 55000,  '2023-03-01', 6,    'F'),
            (16, 'Paul Robinson',    6, 67000,  '2019-06-17', None, 'M'),
            (17, 'Quinn Walker',     1, 85000,  '2017-04-29', 1,    'M'),
            (18, 'Rachel Hall',      2, 74000,  '2021-11-08', 3,    'F'),
            (19, 'Sam Young',        3, 62000,  '2022-07-03', 4,    'M'),
            (20, 'Tina Scott',       5, 89000,  '2016-02-19', 9,    'F'),
        ]
    )

    cur.executemany(
        "INSERT INTO customers (id, name, email, city, country, signup_date) VALUES (?, ?, ?, ?, ?, ?)",
        [
            (1,  'Liam Green',      'liam@example.com',    'New York',     'USA',    '2020-01-15'),
            (2,  'Emma Blue',       'emma@example.com',    'London',       'UK',     '2020-03-22'),
            (3,  'Noah Red',        'noah@example.com',    'Toronto',      'Canada', '2019-11-10'),
            (4,  'Ava White',       'ava@example.com',     'Sydney',       'AU',     '2021-06-05'),
            (5,  'William Black',   'will@example.com',    'Chicago',      'USA',    '2018-08-30'),
            (6,  'Sophia Gold',     'sophia@example.com',  'Paris',        'France', '2022-02-14'),
            (7,  'James Silver',    'james@example.com',   'New York',     'USA',    '2019-05-17'),
            (8,  'Isabella Gray',   'isa@example.com',     'Berlin',       'Germany','2021-09-01'),
            (9,  'Oliver Stone',    'oliver@example.com',  'Chicago',      'USA',    '2020-12-25'),
            (10, 'Mia Fox',         'mia@example.com',     'Toronto',      'Canada', '2022-04-10'),
            (11, 'Elijah Rose',     'elijah@example.com',  'Los Angeles',  'USA',    '2021-07-19'),
            (12, 'Charlotte Moon',  'charlotte@example.com','Sydney',      'AU',     '2018-01-08'),
            (13, 'Lucas Sun',       'lucas@example.com',   'London',       'UK',     '2023-03-30'),
            (14, 'Amelia Star',     'amelia@example.com',  'Paris',        'France', '2020-10-16'),
            (15, 'Mason River',     'mason@example.com',   'Seattle',      'USA',    '2019-02-28'),
        ]
    )

    cur.executemany(
        "INSERT INTO products (id, name, category, price, stock) VALUES (?, ?, ?, ?, ?)",
        [
            (1,  'Laptop Pro 15',    'Electronics', 1299.99, 45),
            (2,  'Wireless Mouse',   'Electronics', 29.99,   200),
            (3,  'Mechanical Keyboard','Electronics',89.99,  120),
            (4,  'Standing Desk',    'Furniture',   499.99,  30),
            (5,  'Office Chair',     'Furniture',   349.99,  50),
            (6,  'Monitor 27"',      'Electronics', 399.99,  75),
            (7,  'Webcam HD',        'Electronics', 79.99,   90),
            (8,  'Notebook Set',     'Stationery',  12.99,   500),
            (9,  'Pen Pack',         'Stationery',  5.99,    1000),
            (10, 'USB-C Hub',        'Electronics', 49.99,   150),
            (11, 'Headphones Pro',   'Electronics', 199.99,  60),
            (12, 'Desk Lamp',        'Furniture',   39.99,   180),
            (13, 'Whiteboard',       'Stationery',  89.99,   40),
            (14, 'Ergonomic Mouse',  'Electronics', 59.99,   110),
            (15, 'Cable Organizer',  'Accessories', 14.99,   300),
        ]
    )

    cur.executemany(
        "INSERT INTO orders (id, customer_id, product_id, quantity, order_date, status, total_amount) VALUES (?, ?, ?, ?, ?, ?, ?)",
        [
            (1,  1,  1,  1,  '2023-01-10', 'Delivered',  1299.99),
            (2,  2,  2,  2,  '2023-01-15', 'Delivered',  59.98),
            (3,  3,  3,  1,  '2023-02-05', 'Delivered',  89.99),
            (4,  1,  6,  2,  '2023-02-20', 'Shipped',    799.98),
            (5,  5,  4,  1,  '2023-03-01', 'Delivered',  499.99),
            (6,  4,  5,  2,  '2023-03-14', 'Delivered',  699.98),
            (7,  7,  11, 1,  '2023-04-02', 'Delivered',  199.99),
            (8,  6,  7,  1,  '2023-04-18', 'Cancelled',  79.99),
            (9,  9,  10, 3,  '2023-05-07', 'Delivered',  149.97),
            (10, 8,  2,  5,  '2023-05-22', 'Delivered',  149.95),
            (11, 10, 1,  1,  '2023-06-01', 'Shipped',    1299.99),
            (12, 11, 8,  10, '2023-06-15', 'Delivered',  129.90),
            (13, 12, 9,  20, '2023-07-03', 'Delivered',  119.80),
            (14, 3,  14, 2,  '2023-07-20', 'Processing', 119.98),
            (15, 15, 12, 1,  '2023-08-05', 'Delivered',  39.99),
            (16, 2,  15, 3,  '2023-08-17', 'Delivered',  44.97),
            (17, 13, 3,  1,  '2023-09-01', 'Shipped',    89.99),
            (18, 14, 6,  1,  '2023-09-14', 'Delivered',  399.99),
            (19, 5,  11, 2,  '2023-10-01', 'Delivered',  399.98),
            (20, 1,  10, 2,  '2023-10-18', 'Delivered',  99.98),
            (21, 7,  5,  1,  '2023-11-05', 'Cancelled',  349.99),
            (22, 9,  1,  1,  '2023-11-20', 'Delivered',  1299.99),
            (23, 4,  2,  4,  '2023-12-01', 'Delivered',  119.96),
            (24, 6,  13, 1,  '2023-12-14', 'Processing', 89.99),
            (25, 11, 4,  1,  '2024-01-07', 'Delivered',  499.99),
        ]
    )

    cur.executemany(
        "INSERT INTO sales (id, employee_id, amount, sale_date, region) VALUES (?, ?, ?, ?, ?)",
        [
            (1,  4,  12500, '2023-01-05', 'North'),
            (2,  8,  9800,  '2023-01-12', 'South'),
            (3,  12, 15200, '2023-01-19', 'West'),
            (4,  4,  11000, '2023-02-03', 'North'),
            (5,  19, 8700,  '2023-02-15', 'East'),
            (6,  8,  13400, '2023-03-01', 'South'),
            (7,  12, 17800, '2023-03-22', 'West'),
            (8,  4,  9500,  '2023-04-10', 'North'),
            (9,  19, 14200, '2023-04-28', 'East'),
            (10, 8,  10100, '2023-05-06', 'South'),
            (11, 12, 19600, '2023-05-17', 'West'),
            (12, 4,  16300, '2023-06-02', 'North'),
            (13, 19, 11900, '2023-06-20', 'East'),
            (14, 8,  12700, '2023-07-08', 'South'),
            (15, 12, 21000, '2023-07-25', 'West'),
            (16, 4,  14800, '2023-08-14', 'North'),
            (17, 19, 9300,  '2023-09-01', 'East'),
            (18, 8,  16500, '2023-09-19', 'South'),
            (19, 12, 18400, '2023-10-07', 'West'),
            (20, 4,  13200, '2023-10-24', 'North'),
            (21, 19, 15700, '2023-11-12', 'East'),
            (22, 8,  11300, '2023-11-29', 'South'),
            (23, 12, 22500, '2023-12-16', 'West'),
            (24, 4,  17900, '2024-01-03', 'North'),
            (25, 19, 13600, '2024-01-21', 'East'),
        ]
    )

    conn.commit()
