import requests
import pandas as pd
from datetime import datetime, timezone, timedelta
import os

# -----------------------------
# Config
# -----------------------------
param_dict = {"pm10": 1, "pm25": 2, "co": 4, "no2": 5}

LIMIT = 1000
BBOX = (76.5, 28.05, 78.29, 29.18)

headers = {
    "accept": "application/json",
    "X-API-Key": "ADD YOUR API KEY HERE"
}

# -----------------------------
# Time: last 3 hours
# -----------------------------
dt_min = (datetime.now(timezone.utc) - timedelta(hours=1)).replace(second=0, microsecond=0)
dt_min_str = dt_min.isoformat().replace("+00:00", "Z")

print("datetime_from:", dt_min_str)

# -----------------------------
# Helper
# -----------------------------
def in_bbox(lon, lat, bbox):
    min_lon, min_lat, max_lon, max_lat = bbox
    return (min_lon <= lon <= max_lon) and (min_lat <= lat <= max_lat)

# -----------------------------
# Store results
# -----------------------------
dfs = {}

# -----------------------------
# Loop over parameters
# -----------------------------
for pname, pid in param_dict.items():
    print(f"\nFetching {pname} (ID={pid})")

    BASE_URL = f"https://api.openaq.org/v3/parameters/{pid}/latest"

    all_results = []
    page = 1

    while True:
        params = {
            "limit": LIMIT,
            "page": page,
            "datetime_from": dt_min_str   # <-- FIXED
        }

        response = requests.get(BASE_URL, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            break

        data = response.json()
        results = data.get("results", [])

        print(f"{pname} | Page {page} → {len(results)}")

        if not results:
            break

        all_results.extend(results)
        page += 1

    # -----------------------------
    # Filter by bbox
    # -----------------------------
    filtered = []
    for r in all_results:
        coords = r.get("coordinates")
        if coords:
            lon = coords.get("longitude")
            lat = coords.get("latitude")
            if lon is not None and lat is not None:
                if in_bbox(lon, lat, BBOX):
                    filtered.append(r)

    print(f"{pname} → Filtered: {len(filtered)}")

    # -----------------------------
    # Convert to DataFrame
    # -----------------------------
    rows = []
    for r in filtered:
        rows.append({
            "datetime_utc": r["datetime"]["utc"],
            "datetime_local": r["datetime"]["local"],
            "value": r["value"],
            "lat": r["coordinates"]["latitude"],
            "lon": r["coordinates"]["longitude"],
            "sensor_id": r["sensorsId"],
            "location_id": r["locationsId"]
        })

    df = pd.DataFrame(rows)

    # store in dict
    dfs[pname] = df

# Get current working directory
base_dir = os.getcwd()

# Create full path
data_dir = os.path.join(base_dir, "data_latest")
os.makedirs(data_dir, exist_ok=True)

for pname, df in dfs.items():
    filename = os.path.join(data_dir, f"{pname}_latest.csv")
    df.to_csv(filename, index=False)
    print(f"Saved {filename}")
# -----------------------------
# Access example
# -----------------------------
pm25_df = dfs["pm25"]
print(pm25_df.head())
