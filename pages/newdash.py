import geopandas as gpd
import folium
import pandas as pd
import numpy as np
from shapely.geometry import Point
from folium.plugins import HeatMap

# -----------------------------
# Load data
# -----------------------------
states = gpd.read_file("india_states.geojson")
df = pd.read_csv("location.csv")

df = df.dropna(subset=["latitude", "longitude"])

# Convert stations to GeoDataFrame
geometry = [Point(xy) for xy in zip(df["longitude"], df["latitude"])]
stations_gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# -----------------------------
# Spatial join → assign state
# -----------------------------
stations_with_state = gpd.sjoin(
    stations_gdf,
    states[["ST_NM", "geometry"]],
    how="left",
    predicate="within"
)

# -----------------------------
# Load AQI data
# -----------------------------
aqi_df = pd.read_csv("india_aqi_data.csv")

# -----------------------------
# AQI Calculation (weighted)
# -----------------------------
def normalize(val, max_val):
    if pd.isna(val):
        return 0
    return min(val / max_val, 1)

weights = {
    "pm25": 0.4,
    "pm10": 0.2,
    "no2": 0.1,
    "so2": 0.1,
    "co": 0.1,
    "o3": 0.1
}

def compute_aqi(row):
    score = 0
    score += normalize(row["pm25"], 250) * weights["pm25"]
    score += normalize(row["pm10"], 300) * weights["pm10"]
    score += normalize(row["no2"], 200) * weights["no2"]
    score += normalize(row["so2"], 200) * weights["so2"]
    score += normalize(row["co"], 10) * weights["co"]
    score += normalize(row["o3"], 180) * weights["o3"]
    return score * 500

aqi_df["aqi"] = aqi_df.apply(compute_aqi, axis=1)

# -----------------------------
# 🔥 FIX: Log scaling + normalization
# -----------------------------
aqi_df["aqi_scaled"] = np.log1p(aqi_df["aqi"])  # amplify contrast
max_val = aqi_df["aqi_scaled"].max()

heat_data = [
    [row["latitude"], row["longitude"], row["aqi_scaled"] / max_val]
    for _, row in aqi_df.iterrows()
    if not pd.isna(row["latitude"]) and not pd.isna(row["longitude"])
]

# -----------------------------
# Create map
# -----------------------------
m = folium.Map(location=[22.5, 79], zoom_start=5, tiles="CartoDB positron")

# -----------------------------
# Add state boundaries
# -----------------------------
folium.GeoJson(
    states,
    zoom_on_click=True,
    style_function=lambda x: {
        "fillOpacity": 0,
        "color": "black",
        "weight": 1
    },
    highlight_function=lambda x: {
        "fillColor": "yellow",
        "fillOpacity": 0.3
    },
    tooltip=folium.GeoJsonTooltip(fields=["ST_NM"])
).add_to(m)

# -----------------------------
# 🔥 Add AQI Heatmap FIRST
# -----------------------------
HeatMap(
    heat_data,
    radius=30,      # stronger spread
    blur=40,        # smoother glow
    min_opacity=0.5
).add_to(m)

# -----------------------------
# Add red station markers (on top)
# -----------------------------
for _, row in stations_with_state.iterrows():
    if pd.isna(row["latitude"]) or pd.isna(row["longitude"]):
        continue

    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=2,
        color="red",
        fill=True,
        fill_color="red",
        fill_opacity=0.9,
        popup=row["name"]
    ).add_to(m)

# -----------------------------
# Save map
# -----------------------------
m.save("india_aqi_heatmap.html")

print("Done → india_aqi_heatmap.html")