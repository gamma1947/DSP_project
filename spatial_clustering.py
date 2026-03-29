import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from scipy.spatial import cKDTree
import ast
import folium
from streamlit_folium import st_folium

# ---------------------------------------------------------
# 1. Setup and Data Caching
# ---------------------------------------------------------
# We use st.cache_data so the CSV and KDTree are only loaded once, 
# making the app extremely fast when you click around.
@st.cache_data
def load_data():
    df = pd.read_csv('delhi_location.csv')
    
    def parse_sensors(sensor_str):
        try:
            return ast.literal_eval(sensor_str)
        except:
            return []
            
    df['parsed_sensors'] = df['sensors'].apply(parse_sensors)
    
    # Build GeoDataFrame
    geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    
    # Build KDTree for fast spatial queries
    sensor_coords = df[['latitude', 'longitude']].values
    tree = cKDTree(sensor_coords)
    
    return df, gdf, tree

df, gdf, tree = load_data()

# ---------------------------------------------------------
# 2. App UI Layout
# ---------------------------------------------------------
st.title("Delhi Air Quality Interpolator 🌫️")
st.write("Click anywhere on the map to find the nearest sensor reading!")

# ---------------------------------------------------------
# 3. Render the Map and Capture Clicks
# ---------------------------------------------------------
# Create a base Folium map centered on Delhi
m = folium.Map(location=[28.6139, 77.2090], zoom_start=11)

# Add our sensors to the map as small red circles so they don't clutter the view
for idx, row in gdf.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=3,
        color='red',
        fill=True,
        tooltip=row['name']
    ).add_to(m)

# st_folium renders the map and returns a dictionary of user interactions!
map_data = st_folium(m, width=700, height=500)

# ---------------------------------------------------------
# 4. Handle the User Input (The Click)
# ---------------------------------------------------------
if map_data and map_data.get("last_clicked"):
    clicked_lat = map_data["last_clicked"]["lat"]
    clicked_lon = map_data["last_clicked"]["lng"]
    
    st.subheader("📍 Your Selected Location")
    st.write(f"**Latitude:** {clicked_lat:.4f} | **Longitude:** {clicked_lon:.4f}")
    
    # Query the KDTree
    distance, index = tree.query([[clicked_lat, clicked_lon]], k=1)
    nearest_sensor = df.iloc[index[0]]
    
    # Calculate distance in approx kilometers (1 degree is ~111km)
    dist_km = distance[0] * 111 
    
    st.success(f"**Nearest Sensor:** {nearest_sensor['name']} (Approx {dist_km:.2f} km away)")
    
    # Display the readings in a nice format
    st.markdown("### 📊 Latest Readings")
    readings = nearest_sensor['parsed_sensors']
    
    if readings:
        # Create a dictionary to display as a clean table
        display_data = {}
        for sensor in readings:
            param = sensor['parameter']['display_name']
            units = sensor['parameter']['units']
            display_data[param] = f"Available ({units})" # Replace with actual value if you have it in your dict
            
        st.table(pd.DataFrame(list(display_data.items()), columns=["Parameter", "Status/Units"]))
    else:
        st.warning("No specific parameter data found for this sensor.")