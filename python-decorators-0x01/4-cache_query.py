import time
import sqlite3
import functools

query_cache = {}

def cache_query(func):
    """
    Decorator to cache the results of database queries.
    """
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):  # Added query as an argument
        if query in query_cache:
            print("Fetching result from cache...")
            return query_cache[query]
        else:
            print("Fetching result from database...")
            result = func(conn, query, *args, **kwargs)
            query_cache[query] = result
            return result
    return wrapper

def with_db_connection(func):
    """
    Decorator to automatically handle database connection and closing.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('mydatabase.db')  # Connect to your database
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # Commit changes if successful
            return result
        except Exception as e:
            conn.rollback()  # Rollback changes if an error occurred
            raise  # Re-raise the exception
        finally:
            conn.close()
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):  # Added query as an argument
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# Example Usage (assuming you have a 'users' table in 'mydatabase.db')
# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print("Users (first call):", users)

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print("Users (second call - from cache):", users_again)

# Example with a different query
users_filtered = fetch_users_with_cache(query="SELECT * FROM users WHERE id = 1")
print("Users (filtered):", users_filtered)
