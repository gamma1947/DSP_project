# Air Quality Dynamics in India: A Spatial-Temporal Dashboard for Urban Sensor Networks

An interactive **Air Quality Monitoring Dashboard** built using real-world environmental sensor data.  
This project was developed as a mini-project for the **DS3294: Data Science Practice** course.

The dashboard ingests data from the **OpenAQ API**, processes it through a robust data-cleaning pipeline, and visualizes spatial and temporal pollution trends using an interactive, web-based interface.

The primary objective is to uncover temporal pollution patterns and spatial variations while addressing real-world data imperfections like outliers, noise, and spatial sparsity.

---

## Project Overview

Urban air quality monitoring relies heavily on heterogeneous sensor networks. Real-world data from these networks often contains issues such as spatial sparsity, missing observations, and sensor noise. 

This project develops a reproducible analytics and visualization pipeline that:
1. Collects air quality data from public sensor networks within India.
2. Focuses on three primary and secondary pollutants impacting public health: PM10, PM2.5, and Ozone (O3).
3. Employs Inverse Distance Weighting (IDW) interpolation to estimate pollutant concentrations in unmonitored areas.
4. Automates the real-time detection of extreme pollution events against official government thresholds.
5. Provides an intuitive drill-down HTML/JavaScript interface for seamless visual analysis.

---

## Technologies Used

* **Backend & Data Processing:** Python, Pandas, GeoPandas.
* **Data Source:** OpenAQ API.
* **Frontend / Dashboard:** HTML, JavaScript, Chart.js.
* **Spatial Analysis:** GeoJSON for spatial filtering, Scipy/NumPy for IDW implementation.

---

## Data Source: OpenAQ API

Air quality observations were obtained from the **OpenAQ platform**, focusing exclusively on monitoring stations located within India via a geospatial filtering approach.

* **Latest Data:** Acquired using a 3-hour window to buffer inconsistencies.
* **Historical Data:** Analyzed for the time range of January 2026 to March 2026.
* **API Pagination:** Looping algorithms were implemented to bypass the API's 1000 data point limit.

---

## Variable Selection

Three pollutants were selected due to their severe health impacts and extensive sensor coverage:

| Pollutant | Description | Reason for Selection |
| :--- | :--- | :--- |
| **PM10** | Particulate Matter <10µm | Captures coarse dust and pollution. |
| **PM2.5** | Particulate Matter <2.5µm | Most harmful to human health. |
| **O3** | Ozone | Secondary pollutant, important for photochemical smog. |

---

## System Architecture

The project follows a modular pipeline architecture:

1. **Data Ingestion** (OpenAQ API)
2. **Temporal Resampling** (Hourly averages)
3. **Data Cleaning & Filtering** (Outlier mitigation, spatial masking)
4. **Spatial Interpolation** (Inverse Distance Weighting)
5. **Extreme Event Detection** (Threshold evaluation)
6. **Frontend Rendering** (HTML, Chart.js)

---

## Data Processing Pipeline

### 1. Data Cleaning & Outlier Mitigation
To mitigate discrepancies caused by bad sensor readings, negative values were removed, and data was capped at the 99th percentile before interpolation.

### 2. Spatial Interpolation (IDW)
To transform point-based measurements into a continuous spatial surface, **Inverse Distance Weighting (IDW)** was utilized. The unsampled grid point is calculated as a weighted average of all available station values, where the weight is defined by the inverse of the distance squared (p=2). A synthetic grid resolution of 0.25 was used to balance computational efficiency with local influence. 

### 3. Grid Generation & Masking
Interpolated values falling outside the official administrative boundaries of India were nullified (NaN) using a spatial mask derived from a high-resolution shapefile.

### 4. Extreme Pollution Detection
Hourly sensor averages are evaluated against government thresholds:
* **PM10:** 100 µg/m³
* **PM2.5:** 60 µg/m³
* **Ozone (O3):** 100 µg/m³
Specific location IDs exceeding these limits are dynamically flagged.

---

## Dashboard Features

The HTML/JS based dashboard provides:

* **Interactive Spatial Mapping:** An interactive map of India with an interpolated heatmap overlay to visualize concentration gradients.
* **Dynamic Drill-Down Navigation:** Users can select a specific state, view regional stations, and click individual stations to instantly load historical time-series data without page navigation.
* **Real-time Charting:** Line charts rendered via Chart.js displaying daily/hourly statistics with zooming, panning, and detailed tooltips.
* **Extreme Pollution Alerts:** A dedicated panel listing stations currently recording pollution events beyond acceptable government limits.

---

## Running the Dashboard

### Clone the Repository
```bash
git clone [https://github.com/gamma1947/aqi_monitoring_dashboard-.git](https://github.com/gamma1947/aqi_monitoring_dashboard-.git)
cd aqi_monitoring_dashboard-
cd pages

```
open india.html

## Author Contributions

* **Ashik Sufaid. S**: Led the backend data ingestion pipeline and implemented the Inverse Distance Weighting (IDW) spatial interpolation to resolve sensor sparsity.
* **Ajay Kasaudhan**: Engineered the interactive user interface and developed all data visualization components, including the dynamic drill-down maps and time-series charts.
* **Hitesh CK**: Responsible for defining and characterizing extreme pollution events, integrating official government threshold logic to automate the real-time detection of critical pollutant levels across the monitoring network.

## Acknowledgements

* **Course Instructor:** Prof. Bedarth Goswami, for guidance throughout the DS3294: Data Science Practice course.
* **AI Assistance:** The authors acknowledge the use of Large Language Models (LLMs), specifically OpenAI's ChatGPT and Google's Gemini, during the development of this project. These tools assisted with code debugging, optimizing scripts, and refining the formatting and prose of the project documentation.All AI-generated content and suggestions were critically reviewed, verified, and edited by the authors to ensure technical accuracy and maintain the integrity of the original scientific contribution.

## Future Enhancements

* **Sensor Calibration Weighting:** Implement a weighting system to account for the reliability and calibration history of different sensor types (e.g., high-fidelity government stations vs. low-cost rural sensors).
* **Temporal Interpolation:** Develop robust methods for handling temporal data holes without introducing misleading assumptions during irregular reporting intervals.
* **Extended Pollutant Tracking:** Expand the pipeline to monitor additional secondary pollutants and meteorological data (temperature, humidity) to better model photochemical smog formations.

## License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.
