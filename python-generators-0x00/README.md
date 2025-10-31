Database Seeder

This script, seed.py, is a utility designed to set up the necessary MySQL database and table structure for the ALX_prodev project and populate it with initial user data.

Purpose

The script performs the following actions:

Connects to a running MySQL server using provided credentials.

Creates the database named ALX_prodev if it does not already exist.

Creates the user_data table within the database, which includes fields for user_id (UUID, Primary Key), name, email (Unique), and age.

Populates the user_data table using a hardcoded list of sample user records. It prevents duplicate entries by checking the email address before insertion.

Prerequisites

Before running this script, ensure you have the following installed:

Python 3

MySQL Server

Python MySQL Connector: Install the necessary library using pip:

pip install mysql-connector-python


Setup and Configuration

The script requires you to update the connection details within the seed.py file.

Configure Credentials: Open seed.py and modify the following variables in the --- Configuration --- section:

DB_HOST: Your MySQL host address (e.g., localhost).

DB_USER: Your MySQL username.

DB_PASSWORD: Your MySQL password.

Verify Data: The sample data is currently hardcoded in the SAMPLE_DATA list within seed.py. Verify that this data is correct before running the script.

Usage

To run the database seeding process, execute the script from your terminal:

python seed.py


The script will output progress messages indicating the database and table creation status, as well as which records were successfully inserted or skipped.
