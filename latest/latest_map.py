import folium
from folium.plugins import MarkerCluster
import pandas as pd

# import your function
from latest_india import get_latest_india   # <-- change this

# -----------------------------
# Create map for one parameter
# -----------------------------
def create_map(df, pname):
    if df.empty:
        print(f"No data for {pname}")
        return None

    # Center map
    center_lat = df["lat"].mean()
    center_lon = df["lon"].mean()

    m = folium.Map(location=[center_lat, center_lon], zoom_start=5)

    marker_cluster = MarkerCluster().add_to(m)

    # Normalize values for coloring
    vmin, vmax = df["value"].min(), df["value"].max()

    def get_color(val):
        # simple normalization → blue (low) to red (high)
        if vmax == vmin:
            return "blue"
        ratio = (val - vmin) / (vmax - vmin)
        if ratio < 0.33:
            return "green"
        elif ratio < 0.66:
            return "orange"
        else:
            return "red"

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=6,
            color=get_color(row["value"]),
            fill=True,
            fill_opacity=0.7,
            popup=(
                f"{pname.upper()}<br>"
                f"Value: {row['value']}<br>"
                f"Lat: {row['lat']:.3f}, Lon: {row['lon']:.3f}"
            )
        ).add_to(marker_cluster)

    return m


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":

    dfs = get_latest_india(nhrs=3)

    maps = {}

    for pname, df in dfs.items():
        print(f"Creating map for {pname}")
        m = create_map(df, pname)

        if m is not None:
            filename = f"{pname}_map.html"
            m.save(filename)
            print(f"Saved {filename}")