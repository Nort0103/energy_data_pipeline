import requests
import json


def test_smard_connection():
    # 4068 is the SMARD filter code for Wind Onshore generation.
    # 1001 is the region code for Germany.
    url = "https://www.smard.de/app/chart_data/4067/DE/index_quarterhour.json"

    headers = {
        "Accept": "application/json"
    }

    print("Initiating connection to SMARD.de API...")

    try:
        response = requests.get(url, headers=headers)

        # Check if the server responded with 200 OK
        if response.status_code == 200:
            print("Success! HTTP 200 OK.")
            data = response.json()

            # The API returns a list of available timestamp files
            timestamps = data.get("timestamps", [])
            print(
                f"Connected successfully. Found {len(timestamps)} data points available for Wind Onshore.")
        else:
            print(
                f"Connection failed. Server returned HTTP Status: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"A network error occurred: {e}")


if __name__ == "__main__":
    test_smard_connection()
