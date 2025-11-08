import asyncio
import aiosqlite

class ExecuteQuery:
    """
    A reusable context manager for executing SQL queries asynchronously.

    Args:
        db_path (str): The path to the SQLite database file.
        query (str): The SQL query to execute.
        params (tuple, optional): The parameters to pass to the query. Defaults to None.
    """

    def __init__(self, db_path: str, query: str, params: tuple = None):
        self.db_path = db_path
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None
        self.result = None

    async def __aenter__(self):
        """
        Asynchronously establishes a database connection and executes the query.

        Returns:
            The result of the query.
        """
        try:
            self.conn = await aiosqlite.connect(self.db_path)
            self.cursor = await self.conn.execute(self.query, self.params)
            self.result = await self.cursor.fetchall()
            return self.result
        except aiosqlite.Error as e:
            print(f"Database error during __aenter__: {e}")
            # Re-raise the exception to be handled by __exit__
            raise
        except Exception as e:
            print(f"An unexpected error occurred during __aenter__: {e}")
            raise # Re-raise to ensure proper cleanup

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Asynchronously closes the database connection, handling potential errors.

        Args:
            exc_type: The exception type (if any).
            exc_val: The exception value (if any).
            exc_tb: The traceback (if any).
        """
        try:
            if self.cursor:
                await self.cursor.close()
            if self.conn:
                await self.conn.close()
        except aiosqlite.Error as e:
            print(f"Error closing database connection: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during __aexit__: {e}")
        # Optionally, re-raise the exception to propagate it
        # if exc_type is not None:
        #     return False  # If you return False, the exception will be re-raised.  If you return True, it will be suppressed.

# Example Usage:
async def main():
    db_path = "users.db"

    # Create a dummy database and table (if it doesn't exist)
    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER
            )
        """)
        await db.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [
            ("Alice", 30),
            ("Bob", 45),
            ("Charlie", 50),
            ("David", 25),
            ("Eve", 60)
        ])
        await db.commit()

    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)  # Corrected: params must be a tuple

    try:
        async with ExecuteQuery(db_path, query, params) as result:
            print("Users older than 25:", result)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
