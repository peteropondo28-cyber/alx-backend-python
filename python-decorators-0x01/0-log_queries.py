import sqlite3
import functools

#### decorator to log SQL queries
def log_queries(func):
    """
    Decorator to log SQL queries before execution.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = args[0]  # Assuming the query is the first argument
        print(f"Executing SQL query: {query}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
# Create a dummy database and table for demonstration
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER
    )
""")
cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [
    ("Alice", 30),
    ("Bob", 45),
    ("Charlie", 50),
    ("David", 25)
])
conn.commit()
conn.close()

users = fetch_all_users(query="SELECT * FROM users")
print(users)
