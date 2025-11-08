import asyncio
import aiosqlite

async def async_fetch_users(db_path: str):
    """Fetches all users from the database."""
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return users

async def async_fetch_older_users(db_path: str):
    """Fetches users older than 40 from the database."""
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            return older_users

async def fetch_concurrently(db_path: str):
    """Executes both queries concurrently using asyncio.gather()."""
    try:
        users, older_users = await asyncio.gather(
            async_fetch_users(db_path),
            async_fetch_older_users(db_path)
        )
        print("All users:", users)
        print("Older users:", older_users)
    except Exception as e:
        print(f"An error occurred: {e}")

# Example Usage (Assuming you have a database file named 'users.db')
async def main():
    # Create a dummy database and table for demonstration
    db_path = "users.db"
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
            ("David", 25)
        ])
        await db.commit()
    await fetch_concurrently(db_path)

if __name__ == "__main__":
    asyncio.run(main())
