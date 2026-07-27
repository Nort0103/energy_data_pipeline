import requests
import pandas as pd
from datetime import datetime
import sqlite3


def get_latest_wind_data():
    index_url = "https://www.smard.de/app/chart_data/4067/DE/index_quarterhour.json"
    headers = {"Accept": "application/json"}

    print("Fetching timestamp index...")
    index_response = requests.get(index_url, headers=headers)
    timestamps = index_response.json().get("timestamps", [])

    if not timestamps:
        print("Error: No timestamps found.")
        return

    latest_timestamp = timestamps[-1]
    data_url = f"https://www.smard.de/app/chart_data/4067/DE/4067_DE_quarterhour_{latest_timestamp}.json"

    print("Downloading Wind Onshore generation data...")
    data_response = requests.get(data_url, headers=headers)
    series_data = data_response.json().get("series", [])

    df = pd.DataFrame(series_data, columns=["Timestamp", "Megawatts"])
    df['Datetime'] = pd.to_datetime(df['Timestamp'], unit='ms')
    df = df[['Datetime', 'Megawatts']]
    df = df.dropna(subset=['Megawatts'])

    print("\nConnecting to local database...")
    db_connection = sqlite3.connect('energy_data.db')

    # --- BULLETPROOF DEDUPLICATION LOGIC ---
    # 1. Ask SQLite's master record if our table exists yet
    table_check_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='wind_onshore'"
    table_exists = not pd.read_sql(table_check_query, db_connection).empty

    if table_exists:
        # 2. Table exists, check for the newest date
        max_date_query = "SELECT MAX(Datetime) FROM wind_onshore"
        max_date_df = pd.read_sql(max_date_query, db_connection)
        max_date_str = max_date_df.iloc[0, 0]

        if max_date_str:
            max_date = pd.to_datetime(max_date_str)
            # Filter the dataframe to ONLY include rows newer than the database
            df = df[df['Datetime'] > max_date]
            print(
                f"Database found. Checking for records newer than {max_date}...")
    else:
        print("No existing table found. Creating fresh database table...")

    # --- INSERTION LOGIC ---
    if not df.empty:
        print(f"Inserting {len(df)} new records...")
        df.to_sql('wind_onshore', con=db_connection,
                  if_exists='append', index=False)
        print("Success! Data securely saved.")
    else:
        print("Database is already up to date. No new records inserted.")

    db_connection.close()


if __name__ == "__main__":
    get_latest_wind_data()
