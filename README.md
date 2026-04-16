# [cite_start]Air Quality Dynamics in India: A Spatial-Temporal Dashboard for Urban Sensor Networks [cite: 1, 2]

[cite_start]An interactive **Air Quality Monitoring Dashboard** built using real-world environmental sensor data[cite: 10].  
[cite_start]This project was developed as a mini-project for the **DS3294: Data Science Practice** course[cite: 3].

[cite_start]The dashboard ingests data from the **OpenAQ API**, processes it through a robust data-cleaning pipeline, and visualizes spatial and temporal pollution trends using an interactive, web-based interface[cite: 12, 15, 204].

[cite_start]The primary objective is to uncover temporal pollution patterns and spatial variations while addressing real-world data imperfections like outliers, noise, and spatial sparsity[cite: 11, 15, 16].

---

## Project Overview

[cite_start]Urban air quality monitoring relies heavily on heterogeneous sensor networks[cite: 18]. [cite_start]Real-world data from these networks often contains issues such as spatial sparsity, missing observations, and sensor noise[cite: 20, 22]. 

This project develops a reproducible analytics and visualization pipeline that:
1. [cite_start]Collects air quality data from public sensor networks within India[cite: 12, 36].
2. [cite_start]Focuses on three primary and secondary pollutants impacting public health: PM10, PM2.5, and Ozone (O3)[cite: 13, 14].
3. [cite_start]Employs Inverse Distance Weighting (IDW) interpolation to estimate pollutant concentrations in unmonitored areas[cite: 75, 76].
4. [cite_start]Automates the real-time detection of extreme pollution events against official government thresholds[cite: 31].
5. [cite_start]Provides an intuitive drill-down HTML/JavaScript interface for seamless visual analysis[cite: 204, 210].

---

## Technologies Used

* [cite_start]**Backend & Data Processing:** Python, Pandas, GeoPandas[cite: 49].
* [cite_start]**Data Source:** OpenAQ API[cite: 35].
* [cite_start]**Frontend / Dashboard:** HTML, JavaScript, Chart.js[cite: 213].
* [cite_start]**Spatial Analysis:** GeoJSON for spatial filtering, Scipy/NumPy for IDW implementation[cite: 49, 140].

---

## Data Source: OpenAQ API

[cite_start]Air quality observations were obtained from the **OpenAQ platform**, focusing exclusively on monitoring stations located within India via a geospatial filtering approach[cite: 35, 36, 48].

* [cite_start]**Latest Data:** Acquired using a 3-hour window to buffer inconsistencies[cite: 51, 52].
* [cite_start]**Historical Data:** Analyzed for the time range of January 2026 to March 2026[cite: 54].
* [cite_start]**API Pagination:** Looping algorithms were implemented to bypass the API's 1000 data point limit[cite: 68].

---

## Variable Selection

[cite_start]Three pollutants were selected due to their severe health impacts and extensive sensor coverage[cite: 14, 46]:

| Pollutant | Description | Reason for Selection |
| :--- | :--- | :--- |
| **PM10** | Particulate Matter $<10\mu m$ | [cite_start]Captures coarse dust and pollution[cite: 39]. |
| **PM2.5** | Particulate Matter $<2.5\mu m$ | [cite_start]Most harmful to human health[cite: 39]. |
| **O3** | Ozone | [cite_start]Secondary pollutant, important for photochemical smog[cite: 39]. |

---

## System Architecture

[cite_start]The project follows a modular pipeline architecture[cite: 204, 205, 206]:

1. **Data Ingestion** (OpenAQ API)
2. **Temporal Resampling** (Hourly averages)
3. **Data Cleaning & Filtering** (Outlier mitigation, spatial masking)
4. **Spatial Interpolation** (Inverse Distance Weighting)
5. **Extreme Event Detection** (Threshold evaluation)
6. **Frontend Rendering** (HTML, Chart.js)

---

## Data Processing Pipeline

### 1. Data Cleaning & Outlier Mitigation
[cite_start]To mitigate discrepancies caused by bad sensor readings, negative values were removed, and data was capped at the 99th percentile before interpolation[cite: 146, 147].

### 2. Spatial Interpolation (IDW)
[cite_start]To transform point-based measurements into a continuous spatial surface, **Inverse Distance Weighting (IDW)** was utilized[cite: 75]. The unsampled grid point is calculated as:
[cite_start]$Z(x_{i},y_{i})=\frac{\sum_{k=1}^{n}w_{k}Z_{k}}{\sum_{k=1}^{n}w_{k}}$ [cite: 80]
[cite_start]A power parameter of $p=2$ and a synthetic grid resolution of 0.25 were used to balance computational efficiency with local influence[cite: 86, 94]. 

### 3. Grid Generation & Masking
[cite_start]Interpolated values falling outside the official administrative boundaries of India were nullified (NaN) using a spatial mask derived from a high-resolution shapefile[cite: 96].

### 4. Extreme Pollution Detection
[cite_start]Hourly sensor averages are evaluated against government thresholds[cite: 221, 223]:
* [cite_start]**PM10:** 100 $\mu g/m^{3}$ [cite: 231]
* [cite_start]**PM2.5:** 60 $\mu g/m^{3}$ [cite: 231]
* [cite_start]**Ozone (O3):** 100 $\mu g/m^{3}$ [cite: 231]
[cite_start]Specific location IDs exceeding these limits are dynamically flagged[cite: 228].

---

## Dashboard Features

[cite_start]The HTML/JS based dashboard provides[cite: 246]:

* [cite_start]**Interactive Spatial Mapping:** An interactive map of India with an interpolated heatmap overlay to visualize concentration gradients[cite: 248, 249].
* [cite_start]**Dynamic Drill-Down Navigation:** Users can select a specific state, view regional stations, and click individual stations to instantly load historical time-series data without page navigation[cite: 250, 251, 268].
* [cite_start]**Real-time Charting:** Line charts rendered via Chart.js displaying daily/hourly statistics with zooming, panning, and detailed tooltips[cite: 213, 214].
* [cite_start]**Extreme Pollution Alerts:** A dedicated panel listing stations currently recording pollution events beyond acceptable government limits[cite: 269, 271].

---

## Running the Dashboard

### Clone the Repository
```bash
git clone [https://github.com/gamma1947/aqi_monitoring_dashboard-.git](https://github.com/gamma1947/aqi_monitoring_dashboard-.git)
cd aqi_monitoring_dashboard-
