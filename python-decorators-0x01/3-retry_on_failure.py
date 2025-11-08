import time
import sqlite3
import functools

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
            raise  # Re-raise the exception to be handled by retry_on_failure
        finally:
            conn.close()
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """
    Decorator to retry a function if it fails due to an exception.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempts + 1} failed: {e}")
                    attempts += 1
                    if attempts < retries:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print("Maximum retry attempts reached.  Raising exception.")
                        raise  # Re-raise the exception after all retries
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    except sqlite3.OperationalError as e:
        # Simulate a transient error (e.g., database locked)
        print(f"Simulating a transient error: {e}")
        raise  # Re-raise the exception to trigger the retry
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

# Example Usage (assuming you have a 'users' table in 'mydatabase.db')
try:
    users = fetch_users_with_retry()
    print(users)
except Exception as e:
    print(f"Failed to fetch users after multiple retries: {e}")
