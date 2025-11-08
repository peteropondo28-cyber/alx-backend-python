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

def transactional(func):
    """
    Decorator that manages database transactions. Commits on success, rolls back on error.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):  # Expects conn as the first argument
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # Commit if the function runs successfully
            return result
        except Exception as e:
            conn.rollback()  # Rollback on any exception
            print(f"Transaction rolled back due to error: {e}")
            raise  # Re-raise the exception to propagate it
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    # Simulate an error for testing rollback
    # if user_id == 999:  # Example: Simulate an error if user_id is 999
    #     raise ValueError("Simulated error during update")
#### Update user's email with automatic transaction handling

# Create a dummy database and table for demonstration
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        email TEXT
    )
""")
cursor.executemany("INSERT INTO users (id, name, age, email) VALUES (?, ?, ?, ?)", [
    (1, "Alice", 30, "alice@example.com"),
    (2, "Bob", 45, "bob@example.com"),
    (3, "Charlie", 50, "charlie@example.com")
])
conn.commit()
conn.close()

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')

# Verify the update (or lack thereof, if an error occurred)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute("SELECT email FROM users WHERE id = ?", (1,))
updated_email = cursor.fetchone()
conn.close()
print(f"Updated email: {updated_email}")
