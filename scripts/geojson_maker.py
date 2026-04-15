# This file was used to separate the states geo json from the india geo json

import json
import os

with open("india_states.geojson") as f:
    data = json.load(f)

os.makedirs("../map/states_geojson", exist_ok=True)

for feature in data["features"]:
    state_name = feature["properties"]["ST_NM"]
    filename = state_name.lower().replace(" ", "") + ".geojson"

    state_geo = {
        "type": "FeatureCollection",
        "features": [feature]
    }

    with open(f"../map/states_geojson/{filename}", "w") as f:
        json.dump(state_geo, f)

print("Done!")