import sqlite3
import functools

def with_db_connection(func):
    """
    Decorator that automatically handles opening and closing database connections.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  # Open the connection
        try:
            # Pass the connection as the first argument to the decorated function
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()  # Close the connection in a finally block to ensure it always closes
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

#### Fetch user by ID with automatic connection handling

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
    (1, "Alice", 30),
    (2, "Bob", 45),
    (3, "Charlie", 50)
])
conn.commit()
conn.close()

user = get_user_by_id(user_id=1)
print(user)
