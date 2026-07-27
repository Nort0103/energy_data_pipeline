import requests
import pandas as pd
from datetime import datetime


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

    # Step 2: Extract the most recent timestamp (the last one in the list)
    latest_timestamp = timestamps[-1]
    print(f"Latest timestamp ID found: {latest_timestamp}")

    # Step 3: Construct the URL for the actual energy data
    data_url = f"https://www.smard.de/app/chart_data/4067/DE/4067_DE_quarterhour_{latest_timestamp}.json"

    print("Downloading Wind Onshore generation data...")
    data_response = requests.get(data_url, headers=headers)
    series_data = data_response.json().get("series", [])

    # Step 4: Convert the raw JSON array into a Pandas DataFrame
    df = pd.DataFrame(series_data, columns=["Timestamp", "Megawatts"])

    # Clean the data: Convert the Unix timestamp to a readable datetime format
    df['Datetime'] = pd.to_datetime(df['Timestamp'], unit='ms')

    # Reorder columns for readability and drop the raw timestamp
    df = df[['Datetime', 'Megawatts']]

    # Drop future time slots or missing sensor data
    df = df.dropna(subset=['Megawatts'])

    print("\n--- Live Wind Onshore Generation (Last 5 records) ---")
    print(df.tail())


if __name__ == "__main__":
    get_latest_wind_data()
