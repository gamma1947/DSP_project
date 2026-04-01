import requests
import pandas as pd
from datetime import datetime, timezone, timedelta
import os
import geopandas as gpd
import shapely
from shapely.geometry import Point
file_path = "ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"
world = gpd.read_file(file_path)
india = world[world["ADMIN"] =="India"]
india_geom = india.geometry.iloc[0]
# -----------------------------
# Config
# -----------------------------
param_dict = {"pm10": 1, "pm25": 2, "o3":3}

LIMIT = 1000

headers = {
    "accept": "application/json",
    "X-API-Key": "703567a9b637449ffb21acf96659f4a58d69761753e4e1082ab6fb84232652de"
}

# -----------------------------
# Loop over parameters
# -----------------------------

def get_latest(nhrs=5, shp_path="ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp", param_dict = {"pm10": 1, "pm25": 2, "o3":3}, save=True ):
    """
    Get the latest data from OpenAQ API 
    nhrs => number of hours before current time to be set as datetime_min for data
    bbox => bounding box of the area of interest
    save => True if save the dataframes else false
    returns a dictionary of dataframes with the param name as key
    """
    dfs = {}
    # -----------------------------
    # Time
    # -----------------------------
    dt_min = (datetime.now(timezone.utc) - timedelta(hours=nhrs)).replace(second=0, microsecond=0)
    dt_min_str = dt_min.isoformat().replace("+00:00", "Z")

    print("datetime_from:", dt_min_str)
    for pname, pid in param_dict.items():
        print(f"\nFetching {pname} (ID={pid})")
    
        BASE_URL = f"https://api.openaq.org/v3/parameters/{pid}/latest"
    
        all_results = []
        page = 1
    
        while True:
            params = {
                "limit": LIMIT,
                "page": page,
                "datetime_min": dt_min_str   # <-- FIXED
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
        # Filter by india
        # -----------------------------
        world = gpd.read_file(file_path)
        india = world[world["ADMIN"] =="India"]
        india_geom = india.geometry.iloc[0]
        filtered = []
        for r in all_results:
            coords = r.get("coordinates")
            if coords:
                lon = coords.get("longitude")
                lat = coords.get("latitude")
                if lon is not None and lat is not None:
                    point = Point(lon, lat)
                    if india_geom.intersects(point):
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
    if save == True:
        # Get current working directory
        base_dir = os.getcwd()
        
        # Create full path
        data_dir = os.path.join(base_dir, "data_latest")
        os.makedirs(data_dir, exist_ok=True)
        
        for pname, df in dfs.items():
            filename = os.path.join(data_dir, f"{pname}_latest_india.csv")
            df.to_csv(filename, index=False)
            print(f"Saved {filename}")
# -----------------------------
# Access example
# -----------------------------
    return dfs

if __name__ == "__main__":
	get_latest()
