import requests
import pandas as pd
from datetime import datetime
import sqlite3


def get_latest_wind_data():
    # Step 1: Get the list of available timestamps
    index_url = "https://www.smard.de/app/chart_data/4067/DE/index_quarterhour.json"
    headers = {"Accept": "application/json"}

    print("Fetching timestamp index...")
    index_response = requests.get(index_url, headers=headers)
    timestamps = index_response.json().get("timestamps", [])

    if not timestamps:
        print("Error: No timestamps found.")
        return

    # Step 2: Extract the most recent timestamp
    latest_timestamp = timestamps[-1]

    # Step 3: Construct the URL and download data
    data_url = f"https://www.smard.de/app/chart_data/4067/DE/4067_DE_quarterhour_{latest_timestamp}.json"

    print("Downloading Wind Onshore generation data...")
    data_response = requests.get(data_url, headers=headers)
    series_data = data_response.json().get("series", [])

    # Step 4: Convert to Pandas DataFrame and clean
    df = pd.DataFrame(series_data, columns=["Timestamp", "Megawatts"])
    df['Datetime'] = pd.to_datetime(df['Timestamp'], unit='ms')
    df = df[['Datetime', 'Megawatts']]
    df = df.dropna(subset=['Megawatts'])

    print("\n--- Live Wind Onshore Generation (Last 5 records) ---")
    print(df.tail())

    # Step 5: Save to SQLite Database
    print("\nConnecting to local database...")
    db_connection = sqlite3.connect('energy_data.db')

    # Write the dataframe to a SQL table named 'wind_onshore'
    # 'append' means it will add new rows to existing data without deleting the old stuff
    df.to_sql('wind_onshore', con=db_connection,
              if_exists='append', index=False)

    db_connection.close()
    print("Success! Data securely saved to energy_data.db")


if __name__ == "__main__":
    get_latest_wind_data()
if __name__ == "__main__":
    get_latest_wind_data()
