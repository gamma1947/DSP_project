from openaq import OpenAQ as aq
import pandas as pd
from functools import reduce
import time
import os
 
# Load API
api = aq(api_key="703567a9b637449ffb21acf96659f4a58d69761753e4e1082ab6fb84232652de")
 
# Parameter mapping: name -> OpenAQ parameter id
param_dict = {"pm10": 1, "pm25": 2, "o3": 3}

# Output directory
os.makedirs("data", exist_ok=True)
 
# Fetch all locations in the bounding box once
locations = api.locations.list(
    bbox=(76.5, 28.05, 78.29, 29.18),
    limit=1000
)
 
locs_data = [loc for loc in locations.results]
df_locs = pd.DataFrame(locs_data)
 
 
def has_param_sensor(sensor_list, param_id):
    """Return True if any sensor in the list measures the given parameter id."""
    if not isinstance(sensor_list, list):
        return False
    for sensor in sensor_list:
        try:
            if sensor["parameter"]["id"] == param_id:
                return True
        except (KeyError, TypeError):
            continue
    return False
 
 
def build_sensor_df(df_locs, param_id, param_name):
    """Extract a clean dataframe of locations + sensor ids for a given parameter."""
    df_filtered = df_locs[
        df_locs["sensors"].apply(lambda s: has_param_sensor(s, param_id))
    ].reset_index(drop=True)
 
    rows = []
    for _, row in df_filtered.iterrows():
        sensors = row["sensors"]
        if not isinstance(sensors, list):
            continue
        for sensor in sensors:
            try:
                if sensor["parameter"]["id"] == param_id:
                    rows.append({
                        "location_id": row["id"],
                        "location_name": row["name"],
                        "latitude": row["coordinates"]["latitude"],
                        "longitude": row["coordinates"]["longitude"],
                        f"{param_name}_sensor_id": sensor["id"]
                    })
            except (KeyError, TypeError):
                continue
 
    return pd.DataFrame(rows)
 
 
def fetch_all_measurements(api, sensor_id, date_from, date_to):
    """Page through the API to collect all measurements for a sensor."""
    all_results = []
    page = 1
    retries = 0
    max_retries = 3

    while True:
        try:
            resp = api.measurements.list(
                sensors_id=sensor_id,
                datetime_from=date_from,
                datetime_to=date_to,
                limit=1000,
                page=page
            ).results
        except Exception as e:
            retries += 1
            if retries >= max_retries:
                print(f"  ⚠️ Max retries reached for sensor {sensor_id} → skipping.")
                return []
            print(f"  ⚠️ Error: {e} → sleeping 10s and retrying... (attempt {retries}/{max_retries})")
            time.sleep(10)
            continue

        retries = 0  # reset on success

        if not resp:
            break

        all_results.extend(resp)

        if len(resp) < 1000:
            break

        page += 1
        time.sleep(0.5)

    return all_results
 
 
def measurements_to_df(results, location_id):
    """Convert raw measurement results to a tidy dataframe."""
    rows = []
    for m in results:
        try:
            rows.append({
                "datetime": m.period.datetime_from.local,
                "value": m.value,
                "location_id": location_id,
            })
        except (KeyError, TypeError):
            continue
    return pd.DataFrame(rows)
 
 
def fetch_and_merge_param(api, df_locs, param_name, param_id, date_from, date_to):
    """Fetch all data for one parameter and return a wide-format merged dataframe."""
    print(f"\n{'='*50}")
    print(f"Processing parameter: {param_name} (id={param_id})")
    print(f"{'='*50}")
 
    df_sensors = build_sensor_df(df_locs, param_id, param_name)
 
    if df_sensors.empty:
        print(f"  No locations found with {param_name} sensors.")
        return None
 
    print(f"  Found {len(df_sensors)} sensor(s).")
 
    sensor_col = f"{param_name}_sensor_id"
    all_dfs = []
 
    for _, row in df_sensors.iterrows():
        sensor_id = row[sensor_col]
        location_id = row["location_id"]
        location_name = row["location_name"]
 
        if pd.isna(sensor_id):
            continue
 
        print(f"  Fetching {location_name} / id={location_id} (sensor {sensor_id})")
 
        results = fetch_all_measurements(api, int(sensor_id), date_from, date_to)
 
        if not results:
            print(f"  ⚠️ No data for {location_name} ({sensor_id})")
            continue
 
        df_loc = measurements_to_df(results, location_id)
        all_dfs.append(df_loc)
 
    if not all_dfs:
        print(f"  ⚠️ No data collected for {param_name}.")
        return None
 
    # Reshape each location's df to wide format (one column per location)
    dfs_reshaped = []
    for df in all_dfs:
        if df.empty:
            continue
        loc_id = df["location_id"].iloc[0]
        df_wide = (
            df[["datetime", "value"]]
            .rename(columns={"value": loc_id})
            .drop_duplicates(subset=["datetime"])
        )
        dfs_reshaped.append(df_wide)
 
    if not dfs_reshaped:
        return None
 
    # Outer merge across all locations on datetime
    df_merged = reduce(
        lambda left, right: pd.merge(left, right, on="datetime", how="outer"),
        dfs_reshaped
    )
    df_merged = df_merged.sort_values("datetime").reset_index(drop=True)
 
    return df_merged
 
 
# ── Main loop ────────────────────────────────────────────────────────────────
 
DATE_FROM = "2026-01-01"
DATE_TO   = "2026-03-25"
 
for param_name, param_id in param_dict.items():
    df_result = fetch_and_merge_param(
        api, df_locs, param_name, param_id, DATE_FROM, DATE_TO
    )
 
    if df_result is not None:
        out_path = os.path.join("data", f"{param_name}.csv")
        df_result.to_csv(out_path, index=False)
        print(f"  ✅ Saved → {out_path}  ({df_result.shape[0]} rows × {df_result.shape[1]} cols)")
    else:
        print(f"  Skipped saving {param_name} (no data).")