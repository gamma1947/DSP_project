import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Page Configuration MUST be the first Streamlit command
st.set_page_config(page_title="Urban Air Dashboard", layout="wide", initial_sidebar_state="collapsed")



# -------------------------
# 🆕 MAP STATE (ADDED)
# -------------------------
if "show_map" not in st.session_state:
    st.session_state.show_map = False

# 3. Clean Enterprise CSS
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background-color: #f4f7fb;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05),
                0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
    padding: 1.5rem !important;
}

h1, h2, h3, p, label {
    color: #1e293b !important;
}

.main-title {
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 20px;
    margin-top: -30px;
    color: #0f172a !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER (MODIFIED)
# -------------------------
head_col1, head_col2, head_col3 = st.columns([7, 1, 1])

with head_col1:
    st.markdown('<div class="main-title">Urban Air Quality Control Center</div>', unsafe_allow_html=True)

# 🆕 MAP BUTTON
with head_col2:
    if not st.session_state.show_map:
        if st.button("🗺️ Map", use_container_width=True):
            st.session_state.show_map = True
    else:
        if st.button("⬅ Back", use_container_width=True):
            st.session_state.show_map = False

# EXISTING LOGOUT
with head_col3:
    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.switch_page("../main.py")

# -------------------------
# VIEW SWITCH (ADDED)
# -------------------------
if st.session_state.show_map:
    import streamlit.components.v1 as components

    st.subheader("Interactive India Map")

    try:
        with open("../india_map.html", "r", encoding="utf-8") as f:
            html_data = f.read()

        components.html(html_data, height=700, scrolling=True)

    except FileNotFoundError:
        st.error("india_map.html not found. Put it in project folder.")

else:
    # -------------------------
    # ORIGINAL DASHBOARD (UNCHANGED)
    # -------------------------

    # --- TOP FILTER ROW ---
    f1, f2, f3, f4, f5 = st.columns([1, 1, 1, 1.5, 0.8])

    with f1: city = st.selectbox("City:", ["Pune", "Mumbai", "Delhi"], label_visibility="collapsed")
    with f2: source = st.selectbox("Source:", ["Sensor Network", "Satellite", "CBP"], label_visibility="collapsed")
    with f3: pollutant = st.selectbox("Pollutant:", ["PM 2.5", "PM 10", "NO2"], label_visibility="collapsed")
    with f4: date = st.date_input("Date:", [], label_visibility="collapsed")
    with f5: fetch_btn = st.button("Fetch Data", use_container_width=True)

    st.write("")

    # --- DATA ---
    np.random.seed(hash(city + pollutant) % (2 ** 32))

    base_val = 150 if city == "Delhi" else (100 if city == "Mumbai" else 80)
    current_pm25 = int(np.random.normal(base_val, 20))
    current_pm10 = int(current_pm25 * 1.4)
    aqi = int(current_pm25 * 1.2)

    if aqi < 100:
        aqi_status, aqi_color = "Good", "#10b981"
    elif aqi < 200:
        aqi_status, aqi_color = "Moderate", "#f59e0b"
    else:
        aqi_status, aqi_color = "Poor", "#ef4444"

    # --- METRICS ---
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        with st.container(border=True):
            st.markdown(f"**PM 2.5**  \n{current_pm25} µg/m³")

    with m2:
        with st.container(border=True):
            st.markdown(f"**{pollutant}**  \n{current_pm10} µg/m³")

    with m3:
        with st.container(border=True):
            st.markdown(f"**AQI**  \n{aqi} ({aqi_status})")

    with m4:
        with st.container(border=True):
            st.markdown(f"**Temp**  \n{np.random.randint(25, 38)}°C")

    # --- CHART ---
    c_left, c_right = st.columns([2.5, 1])

    with c_left:
        df = pd.DataFrame({
            "Time": [f"{i}:00" for i in range(10)],
            "Level": np.random.randint(50, 200, 10)
        })
        fig = px.area(df, x="Time", y="Level")
        st.plotly_chart(fig, use_container_width=True)

    with c_right:
        if aqi > 150:
            st.error(f"⚠️ High {pollutant} detected in {city}")
        else:
            st.success(f"✅ Air quality stable")

        st.warning("🔋 Sensor battery low")
        st.info(f"🔄 Source: {source}")