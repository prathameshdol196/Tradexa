import sqlite3
from threading import Thread

# Input data for each table
users_data = [
    (1, 'Alice', 'alice@example.com'),
    (2, 'Bob', 'bob@example.com'),
    (3, 'Charlie', 'charlie@example.com'),
    (4, 'David', 'david@example.com'),
    (5, 'Eve', 'eve@example.com'),
    (6, 'Frank', 'frank@example.com'),
    (7, 'Grace', 'grace@example.com'),
    (8, 'Alice', 'alice@example.com'),
    (9, 'Henry', 'henry@example.com'),
    (10, 'Jane', 'jane@example.com')
]

products_data = [
    (1, 'Laptop', 1000.00),
    (2, 'Smartphone', 700.00),
    (3, 'Headphones', 150.00),
    (4, 'Monitor', 300.00),
    (5, 'Keyboard', 50.00),
    (6, 'Mouse', 30.00),
    (7, 'Laptop', 1000.00),
    (8, 'Smartwatch', 250.00),
    (9, 'GamingChair', 500.00),
    (10, 'Earbuds', 50.00)
]

orders_data = [
    (1, 1, 1, 2),
    (2, 2, 2, 1),
    (3, 3, 3, 5),
    (4, 4, 4, 1),
    (5, 5, 5, 2),
    (6, 6, 6, 1),
    (7, 7, 7, 3),
    (8, 8, 8, 2),
    (9, 9, 9, 4),
    (10, 10, 10, 1)
]

# Create database and tables
def setup_database():
    databases = {
        "users.db": "CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)",
        "products.db": "CREATE TABLE IF NOT EXISTS Products (id INTEGER PRIMARY KEY, name TEXT, price REAL)",
        "orders.db": "CREATE TABLE IF NOT EXISTS Orders (id INTEGER PRIMARY KEY, user_id INTEGER, product_id INTEGER, quantity INTEGER)"
    }

    for db_name, table_query in databases.items():
        with sqlite3.connect(db_name) as conn:
            conn.execute(table_query)

# Insert data into tables
def insert_data(db_name, table_name, data):
    with sqlite3.connect(db_name) as conn:
        placeholders = ", ".join(["?"] * len(data[0]))
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        for record in data:
            try:
                conn.execute(query, record)
                print(f"Inserted into {table_name}: {record}")
            except sqlite3.IntegrityError as e:
                print(f"Failed to insert {record} into {table_name}: {e}")

# Run insertions concurrently
def run_concurrent_insertions():
    tables = [
        ("users.db", "Users", users_data),
        ("products.db", "Products", products_data),
        ("orders.db", "Orders", orders_data)
    ]

    threads = [Thread(target=insert_data, args=table) for table in tables]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    setup_database()
    run_concurrent_insertions()
