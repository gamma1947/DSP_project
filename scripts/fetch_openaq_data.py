import pandas as pd
from openaq import OpenAQ
import time

api = OpenAQ(api_key="YOUR_API_KEY")

df = pd.read_csv("../unused_fIles/data/full_location_info.csv")

df["latitude"] = df["coordinates"].apply(
    lambda x: eval(x).get("latitude") if isinstance(x, str) else None
)
df["longitude"] = df["coordinates"].apply(
    lambda x: eval(x).get("longitude") if isinstance(x, str) else None
)

df = df.dropna(subset=["latitude", "longitude"])

data = []

# -----------------------------
# NEW APPROACH (IMPORTANT)
# -----------------------------
for _, row in df.iterrows():
    location_id = row["id"]

    entry = {
        "name": row["name"],
        "latitude": row["latitude"],
        "longitude": row["longitude"]
    }

    try:
        res = api.latest.locations(locations_id=location_id)

        if res.results:
            measurements = res.results[0]["measurements"]

            for m in measurements:
                param = m["parameter"]
                entry[param] = m["value"]

    except:
        pass

    data.append(entry)

    print(entry)

    time.sleep(0.1)

# -----------------------------
# Save
# -----------------------------
final_df = pd.DataFrame(data)

final_df.to_csv("india_aqi_data.csv", index=False)

print("Saved → india_aqi_data.csv")