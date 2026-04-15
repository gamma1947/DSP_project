import requests
import pandas as pd
from datetime import datetime, timedelta, timezone

# --- CONFIG ---
API_KEY = "703567a9b637449ffb21acf96659f4a58d69761753e4e1082ab6fb84232652de"
POLLUTANTS = {"pm25": 2, "pm10": 1, "o3": 3}
DAYS_AGO = 2  # Use 2 days ago to ensure data is fully processed


def get_national_hourly():
    target_day = datetime.now(timezone.utc) - timedelta(days=DAYS_AGO)
    date_str = target_day.strftime('%Y-%m-%d')

    # OpenAQ v3 date format
    date_from = f"{date_str}T00:00:00Z"
    date_to = f"{date_str}T23:59:59Z"

    print(f"Targeting India Data for: {date_str}")

    headers = {"X-API-Key": API_KEY, "Accept": "application/json"}
    final_df = pd.DataFrame({'hour': range(24)})

    for name, pid in POLLUTANTS.items():
        print(f"Fetching {name.upper()}...")

        # v3 stable endpoint for filtering by country and parameter
        url = "https://api.openaq.org/v3/locations"
        params = {
            "countries_id": 9,
            "parameters_id": pid,
            "limit": 100  # Get up to 100 locations in India
        }

        try:
            # Step 1: Get Locations in India that measure this pollutant
            loc_res = requests.get(url, headers=headers, params=params)
            if loc_res.status_code != 200:
                print(f"-> Error fetching locations: {loc_res.status_code}")
                continue

            locations = loc_res.json().get("results", [])
            all_values = []

            # Step 2: For the first few locations, get hourly data
            # (Fetching all would be too slow, 5-10 gives a good national sample)
            for loc in locations[:10]:
                loc_id = loc['id']
                # find the specific sensor ID for this parameter at this location
                sensor = next((s for s in loc['sensors'] if s['parameter']['id'] == pid), None)
                if not sensor: continue

                sensor_id = sensor['id']
                # Fetch hourly averages for this specific sensor
                meas_url = f"https://api.openaq.org/v3/sensors/{sensor_id}/hours"
                meas_params = {"date_from": date_from, "date_to": date_to, "limit": 100}

                meas_res = requests.get(meas_url, headers=headers, params=meas_params)
                if meas_res.status_code == 200:
                    data = meas_res.json().get("results", [])
                    for r in data:
                        hr = pd.to_datetime(r["period"]["datetimeTo"]["utc"]).hour
                        all_values.append({"hour": hr, "value": r["value"]})

            if all_values:
                temp_df = pd.DataFrame(all_values)
                hourly_avg = temp_df.groupby('hour')['value'].mean().reset_index()
                hourly_avg.columns = ['hour', name]
                final_df = pd.merge(final_df, hourly_avg, on='hour', how='left')
                print(f"-> Success: Processed data for {name}")
            else:
                print(f"-> No hourly data found for {name} on this date.")

        except Exception as e:
            print(f"-> Connection Failed: {e}")

    final_df = final_df.fillna(0)
    final_df.to_csv("yesterday_hourly_trend.csv", index=False)
    print("\n--- DONE ---")
    print(final_df)


if __name__ == "__main__":
    get_national_hourly()