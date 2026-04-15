import requests
import json
import os
from datetime import datetime

# --- CONFIG ---
API_KEY = "703567a9b637449ffb21acf96659f4a58d69761753e4e1082ab6fb84232652de"
PARAMS = {"pm25": 2, "pm10": 1, "o3": 3}
BBOX = "68.1,6.7,97.4,35.5"  # India Bounding Box


def fetch_and_save_live_data():
    headers = {"X-API-Key": API_KEY, "Accept": "application/json"}
    live_results = {}

    for name, pid in PARAMS.items():
        url = f"https://api.openaq.org/v3/parameters/{pid}/latest?limit=1000&bbox={BBOX}"
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                values = [r['value'] for r in data.get('results', []) if r['value'] >= 0]

                if values:
                    avg = sum(values) / len(values)
                    live_results[name] = round(avg)
                else:
                    live_results[name] = "N/A"
            else:
                print(f"Error fetching {name}: {response.status_code}")
        except Exception as e:
            print(f"Connection error for {name}: {e}")

    # Save to a JSON file that JS can read easily
    live_results["timestamp"] = datetime.now().strftime("%I:%M %p")

    with open("live_aqi_data.json", "w") as f:
        json.dump(live_results, f)

    print(f"Successfully updated live_aqi_data.json at {live_results['timestamp']}")


if __name__ == "__main__":
    fetch_and_save_live_data()