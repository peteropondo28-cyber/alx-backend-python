import mysql.connector
import uuid
from typing import Optional, List, Dict, Any

# --- Configuration ---
# !!! IMPORTANT: Replace these placeholders with your actual MySQL server credentials !!!
DB_HOST = "localhost"
DB_USER = "your_mysql_user"
DB_PASSWORD = "your_mysql_password"
DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"

# Hardcoded Sample Data (Based on the fields: name, email, age)
# Data transcribed from the provided screenshot.
SAMPLE_DATA = [
    {"name": "Johnnie Hayes", "email": "moss.reynolds@hotmail.com", "age": 55.0},
    {"name": "Myrtle Waters", "email": "edmund.funk@gmail.com", "age": 39.0},
    {"name": "Flora Rodriguez", "email": "willie.bogisich@gmail.com", "age": 44.0},
    {"name": "Dr. Cecilia Konopelski-Larkin", "email": "felicia75@gmail.com", "age": 67.0},
    {"name": "Chelsea Boyle-Stoltenberg", "email": "negira.emard@yahoo.com", "age": 83.0},
    {"name": "Seth Yrlaz", "email": "cecilia.blanka@gmail.com", "age": 74.0},
    {"name": "Thelma Krig-Schinner", "email": "johnnie.jacob@hotmail.com", "age": 36.0},
    {"name": "Thomas Hare", "email": "dominic4@yahoo.com", "age": 33.0},
    {"name": "Delia Hichle", "email": "leon.rohrer@hotmail.com", "age": 35.0},
    {"name": "Kristi Durgan", "email": "marla.schmeler@hotmail.com", "age": 70.0},
    {"name": "Brad Savoye", "email": "dylen.dach@gmail.com", "age": 112.0},
    {"name": "Isabel Crist Jr.", "email": "cecilia.braun54@yahoo.com", "age": 63.0},
    {"name": "Allen Roof", "email": "sandra.heidenreich@gmail.com", "age": 40.0},
    {"name": "Robin Wilkinson", "email": "brent.wilkinson@gmail.com", "age": 62.0},
    {"name": "Martin Flatley", "email": "gabriel2@hotmail.com", "age": 13.0},
    {"name": "Delia Walker Jr.", "email": "leticia.schinner@yahoo.com", "age": 76.0},
    {"name": "Blanca Durgan", "email": "christina78@gmail.com", "age": 31.0},
    {"name": "Ellen Hudson", "email": "matthew.nedhurst@gmail.com", "age": 11.0},
    {"name": "Bobby Bayer", "email": "erick.brekke@gmail.com", "age": 110.0},
    {"name": "Karen Pfannershill", "email": "zemer.steuber-greenfelder@gmail.com", "age": 49.0},
    {"name": "Vanessa Kiln-Durgan", "email": "lorena.schuppe@hotmail.com", "age": 49.0},
    {"name": "Grace Sporer", "email": "george8@yahoo.com", "age": 50.0},
    {"name": "Krista Herzog-Paucek", "email": "shawn.tremblay@hotmail.com", "age": 109.0},
    {"name": "Doyle Schaden", "email": "clarence.berge@hotmail.com", "age": 50.0},
    {"name": "Beth Crooks", "email": "sean.bradts@hotmail.com", "age": 36.0},
    {"name": "Doyle Botsford", "email": "wilfred.dickinson@hotmail.com", "age": 70.0},
    {"name": "Santos Skiles", "email": "joey2@gmail.com", "age": 17.0},
    {"name": "Ms. Gina Hukd", "email": "webbie@hotmail.com", "age": 78.0},
    {"name": "Garry Pfeffer", "email": "llora.heathcote4@yahoo.com", "age": 105.0},
    {"name": "Jennie Raggins", "email": "june.kuhn24@hotmail.com", "age": 92.0},
    {"name": "Hubert Gerlach", "email": "alice2@hotmail.com", "age": 3.0},
    {"name": "Clark Wilkes", "email": "leo55@gmail.com", "age": 45.0},
    {"name": "Natalie Lesch PhD", "email": "marilyn7@yahoo.com", "age": 76.0},
    {"name": "Pauline Cremin", "email": "geraldine.langworth87@hotmail.com", "age": 50.0},
    {"name": "Nellie Labadie", "email": "clay75@hotmail.com", "age": 37.0},
    {"name": "Felipe Barrows", "email": "clint3@yahoo.com", "age": 47.0},
    {"name": "Derrick Mitchell Jr.", "email": "may.fritsch2@hotmail.com", "age": 52.0},
    {"name": "James Boehm", "email": "terry@hotmail.com", "age": 54.0},
]


def connect_db(database: Optional[str] = None) -> Optional[mysql.connector.connection.MySQLConnection]:
    """
    Connects to the MySQL database server (or a specific database).

    :param database: The name of the database to connect to. If None, connects to the server only.
    :return: A MySQLConnection object or None if connection fails.
    """
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=database if database else None
        )
        if connection.is_connected():
            print(f"Successfully connected to MySQL server (Database: {database or 'Server Only'})")
            return connection
        return None
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        print("Please check your DB_HOST, DB_USER, and DB_PASSWORD configurations.")
        return None

def create_database(connection: mysql.connector.connection.MySQLConnection) -> None:
    """
    Creates the database ALX_prodev if it does not exist.

    :param connection: The connection to the MySQL server (must not be connected to DB_NAME).
    """
    cursor = connection.cursor()
    try:
        # Use IF NOT EXISTS to prevent errors if the database already exists
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database '{DB_NAME}' checked/created successfully.")
    except mysql.connector.Error as err:
        print(f"Failed to create database: {err}")
    finally:
        cursor.close()

def connect_to_prodev() -> Optional[mysql.connector.connection.MySQLConnection]:
    """
    Connects to the ALX_prodev database in MySQL.

    :return: A MySQLConnection object connected to ALX_prodev or None.
    """
    return connect_db(database=DB_NAME)

def create_table(connection: mysql.connector.connection.MySQLConnection) -> None:
    """
    Creates the 'user_data' table if it does not exist with the required fields.

    :param connection: The connection to the ALX_prodev database.
    """
    cursor = connection.cursor()
    # SQL to create the table
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        user_id CHAR(36) NOT NULL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE, -- Added UNIQUE constraint to email for safe re-running
        age DECIMAL(5, 2) NOT NULL
    ) ENGINE=InnoDB;
    """
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print(f"Table '{TABLE_NAME}' checked/created successfully.")
    except mysql.connector.Error as err:
        print(f"Failed to create table: {err}")
    finally:
        cursor.close()

def insert_data(connection: mysql.connector.connection.MySQLConnection, data: List[Dict[str, Any]]) -> None:
    """
    Inserts data into the user_data table.

    It first checks if a user with the given email already exists to prevent duplicates.

    :param connection: The connection to the ALX_prodev database.
    :param data: A list of dictionaries containing user data (name, email, age).
    """
    cursor = connection.cursor()
    insert_query = f"""
    INSERT INTO {TABLE_NAME} (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """
    check_query = f"SELECT user_id FROM {TABLE_NAME} WHERE email = %s"
    inserted_count = 0

    print(f"\nAttempting to insert {len(data)} records...")

    for record in data:
        email = record['email']
        name = record['name']
        age = record['age']

        # 1. Check if record already exists by email
        cursor.execute(check_query, (email,))
        if cursor.fetchone() is not None:
            print(f"Skipping: User with email '{email}' already exists.")
            continue

        # 2. If it doesn't exist, generate UUID and insert
        new_uuid = str(uuid.uuid4())
        try:
            cursor.execute(insert_query, (new_uuid, name, email, age))
            print(f"Inserted: {name} ({new_uuid})")
            inserted_count += 1
        except mysql.connector.Error as err:
            # Handle potential database errors (e.g., if another process inserted the email)
            print(f"Error inserting data for {email}: {err}")

    # Commit the changes to the database
    connection.commit()
    print(f"\nDatabase seeding complete. Total new records inserted: {inserted_count}.")
    cursor.close()


if __name__ == "__main__":
    # 1. Connect to MySQL Server (no specific database selected yet)
    server_conn = connect_db()

    if server_conn:
        # 2. Create the database
        create_database(server_conn)
        server_conn.close() # Close the server connection

        # 3. Connect directly to the newly created database (ALX_prodev)
        db_conn = connect_to_prodev()

        if db_conn:
            try:
                # 4. Create the table
                create_table(db_conn)

                # 5. Insert the hardcoded sample data
                data_to_insert = SAMPLE_DATA

                if data_to_insert:
                    insert_data(db_conn, data_to_insert)
                else:
                    print("No sample data available. Skipping insertion.")


            finally:
                # 6. Close the database connection
                if db_conn and db_conn.is_connected():
                    db_conn.close()
                    print("Database connection closed.")
        else:
            print("Failed to connect to the ALX_prodev database. Exiting.")
    else:
        print("Failed to connect to the MySQL server. Cannot proceed with seeding. Exiting.")
