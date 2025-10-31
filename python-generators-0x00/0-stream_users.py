import mysql.connector
from typing import Iterator, Dict, Any

# --- Configuration (Use the same settings as seed.py) ---
# !!! IMPORTANT: Replace these placeholders with your actual MySQL server credentials !!!
DB_HOST = "localhost"
DB_USER = "your_mysql_user"
DB_PASSWORD = "your_mysql_password"
DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"


def stream_users() -> Iterator[Dict[str, Any]]:
    """
    Connects to the ALX_prodev database and streams user rows one by one
    from the 'user_data' table using a Python generator.

    Yields:
        Dict[str, Any]: A dictionary representing a single user row.
    """
    connection = None
    cursor = None
    try:
        # 1. Establish database connection
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if not connection.is_connected():
            raise ConnectionError("Failed to connect to the ALX_prodev database.")

        # 2. Create cursor with 'buffered=False' and 'dictionary=True'
        # 'buffered=False' is crucial for streaming large datasets.
        # 'dictionary=True' makes results easier to work with (keys are column names).
        cursor = connection.cursor(buffered=False, dictionary=True)

        # 3. Execute the query
        print("Executing streaming query...")
        select_query = f"SELECT user_id, name, email, age FROM {TABLE_NAME} ORDER BY name"
        cursor.execute(select_query)

        # 4. Use the cursor as an iterable to stream rows (This uses only 1 implicit loop)
        for row in cursor:
            # 5. Yield each row immediately
            yield row

    except mysql.connector.Error as err:
        print(f"MySQL Error during streaming: {err}")
        print("Ensure the database and table exist and connection details are correct.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # 6. Ensure resources are closed
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("\nDatabase connection closed.")


# Example usage:
if __name__ == "__main__":
    print(f"--- Streaming users from '{DB_NAME}.{TABLE_NAME}' ---")
    
    # Iterate over the generator to process users one at a time
    user_count = 0
    for user in stream_users():
        user_count += 1
        # Process the streamed row immediately
        print(f"User {user_count}: {user['name']} (Email: {user['email']}, Age: {user['age']})")
        
        # Simulating some heavy processing work here
        # time.sleep(0.01)

    print(f"\n--- Streaming complete. Total users processed: {user_count} ---")
