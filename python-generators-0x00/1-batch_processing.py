import mysql.connector
from typing import Iterator, Dict, Any, List, Optional

# --- Configuration (Use the same settings as seed.py) ---
# !!! IMPORTANT: Replace these placeholders with your actual MySQL server credentials !!!
DB_HOST = "localhost"
DB_USER = "your_mysql_user"
DB_PASSWORD = "your_mysql_password"
DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"


def stream_users_in_batches(batch_size: int) -> Iterator[List[Dict[str, Any]]]:
    """
    Connects to the ALX_prodev database and streams user rows in batches
    from the 'user_data' table using a Python generator.

    This function uses 1 loop (while True) to fetch all data in chunks.

    :param batch_size: The number of rows to fetch in each batch.
    Yields:
        List[Dict[str, Any]]: A list of user dictionaries representing a batch.
    """
    connection: Optional[mysql.connector.connection.MySQLConnection] = None
    cursor: Optional[mysql.connector.cursor.MySQLCursor] = None

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
        cursor = connection.cursor(buffered=False, dictionary=True)

        # 3. Execute the query
        print(f"Executing streaming query in batches of {batch_size}...")
        select_query = f"SELECT user_id, name, email, age FROM {TABLE_NAME} ORDER BY age"
        cursor.execute(select_query)

        # 4. Use a single loop to repeatedly fetch and yield batches
        while True: # Loop 1
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break  # Stop when fetchmany returns an empty list
            yield batch

    except mysql.connector.Error as err:
        print(f"MySQL Error during batch streaming: {err}")
        print("Ensure the database and table exist and connection details are correct.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # 5. Ensure resources are closed
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("\nDatabase connection closed.")


def batch_processing(batch_size: int) -> Iterator[Dict[str, Any]]:
    """
    Processes batches of user data, filtering for users over the age of 25.

    This function uses 2 nested loops (one for batches, one for rows).

    :param batch_size: The size of the batches to process.
    Yields:
        Dict[str, Any]: A dictionary representing a single filtered user row.
    """
    # Loop 2: Iterates over the generator that yields batches
    for batch in stream_users_in_batches(batch_size):
        # Loop 3: Iterates over the individual users within the batch
        for user in batch:
            # Note: Age is stored as DECIMAL and fetched as such (often Python's Decimal type or float)
            if float(user['age']) > 25:
                yield user


# Example usage:
if __name__ == "__main__":
    BATCH_SIZE = 5
    
    print(f"--- Processing users over age 25 in batches of {BATCH_SIZE} ---")
    
    # Iterate over the final generator to consume filtered users one at a time
    filtered_count = 0
    
    # This block represents the 3rd and final loop (the consumer loop)
    for user in batch_processing(BATCH_SIZE): 
        filtered_count += 1
        # Process the streamed row immediately
        print(f"Filtered User {filtered_count}: {user['name']} (Age: {user['age']})")
        
        # Simulating some processing work here
        # time.sleep(0.01)

    print(f"\n--- Batch processing complete. Total users over 25: {filtered_count} ---")
