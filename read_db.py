import sqlite3
import pandas as pd


def check_database():
    print("Connecting to database...")
    conn = sqlite3.connect('energy_data.db')

    # Write a standard SQL query to get the 10 most recent records
    query = "SELECT * FROM wind_onshore ORDER BY Datetime DESC LIMIT 10"

    # Use pandas to execute the SQL query and format the output
    df = pd.read_sql(query, conn)

    print("\n--- Data successfully retrieved from SQLite ---")
    print(df)

    # Always close the connection
    conn.close()


if __name__ == "__main__":
    check_database()
