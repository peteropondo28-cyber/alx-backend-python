import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type:
                self.conn.rollback()  # Rollback on error
            else:
                self.conn.commit()  # Commit if no error
            self.cursor.close()
            self.conn.close()

# Example Usage
if __name__ == '__main__':
    # Create a sample database and table (if they don't exist)
    db_name = 'example.db'
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT
            )
        ''')
        # Insert some sample data
        cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (1, 'Alice', 'alice@example.com')")
        cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (2, 'Bob', 'bob@example.com')")
        conn.commit()

    # Using the context manager
    try:
        with DatabaseConnection(db_name) as cursor:
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
            print("User Data:")
            for row in results:
                print(row)
    except Exception as e:
        print(f"An error occurred: {e}")
