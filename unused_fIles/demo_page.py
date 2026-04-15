import folium
import geopandas as gpd
from shapely.geometry import Point
import random
from folium.plugins import HeatMap

# -----------------------------
# Load GeoJSON
# -----------------------------
geojson_path = "../map/india_states.geojson"  # <-- your file

gdf = gpd.read_file(geojson_path)

# -----------------------------
# Check column names (IMPORTANT)
# -----------------------------
print(gdf.columns)

# -----------------------------
# Select state
# -----------------------------
state_name = "Maharashtra"  # change as needed

# Adjust column name if needed
state = gdf[gdf["ST_NM"] == state_name]

if state.empty:
    raise ValueError("State not found. Check column name.")

state_geom = state.geometry.iloc[0]

# -----------------------------
# Generate dummy points INSIDE state
# -----------------------------
minx, miny, maxx, maxy = state_geom.bounds

points = []

while len(points) < 300:
    lat = random.uniform(miny, maxy)
    lon = random.uniform(minx, maxx)

    p = Point(lon, lat)

    if state_geom.contains(p):
        aqi = int(random.randint(50, 300))
        points.append([lat, lon, aqi])

# -----------------------------
# Create map centered on state
# -----------------------------
center = [state_geom.centroid.y, state_geom.centroid.x]

m = folium.Map(location=center, zoom_start=6)

# -----------------------------
# Add state boundary (GeoJSON)
# -----------------------------
folium.GeoJson(
    state,
    name="State Boundary",
    style_function=lambda x: {
        "fillColor": "none",
        "color": "black",
        "weight": 2
    }
).add_to(m)

# -----------------------------
# Add heatmap
# -----------------------------
HeatMap(
    points,
    radius=12,
    blur=15
).add_to(m)

# -----------------------------
# Save
# -----------------------------
m.save(f"{state_name}_heatmap.html")

print(f"✅ Heatmap saved for {state_name}")