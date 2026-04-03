import streamlit as st
import numpy as np

st.set_page_config(page_title="State Dashboard", layout="wide")

# Get state from URL
query_params = st.query_params
state = query_params.get("name", "Unknown")

st.title(f"📍 {state} Air Quality Dashboard")

# Dummy data (replace later with real API)
np.random.seed(hash(state) % (2**32))

aqi = np.random.randint(50, 300)
pm25 = np.random.randint(20, 200)
temp = np.random.randint(20, 40)

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("AQI", aqi)
col2.metric("PM2.5", pm25)
col3.metric("Temperature", f"{temp}°C")

# Back button
if st.button("⬅ Back to Map"):
    st.switch_page("pages/dashboard.py")