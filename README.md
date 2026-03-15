# 🌍 Air Quality Monitoring Dashboard

An interactive **Air Quality Monitoring Dashboard** built using real-world environmental sensor data.  
This project was developed as part of the **Data Science Practices course** taught by Prof. Bedarth Goswami at IISER Pune.

The dashboard ingests data from **OpenAQ**, processes it through a structured data-cleaning pipeline, and visualizes pollution trends using an interactive web interface built with **Streamlit**.

The goal of the project is to understand **temporal pollution patterns, spatial variation across monitoring stations, and the impact of imperfect sensor data on environmental interpretation.**

---

# 📊 Project Overview

Urban air quality monitoring relies heavily on distributed sensor networks that collect environmental data across different locations and time intervals. However, such real-world data often contains issues such as:

- Missing observations  
- Sensor noise  
- Calibration drift  
- Inconsistent reporting frequencies  

This project develops a **reproducible data pipeline and visualization dashboard** that:

1. Collects air quality data from public sensor networks  
2. Cleans and harmonizes the data  
3. Handles missing and noisy readings  
4. Aggregates pollution data across different time scales  
5. Provides interactive visualizations for exploration and analysis  

---

# ⚙️ Technologies Used

- Python  
- Streamlit — interactive dashboard interface  
- OpenAQ API — air quality data source  
- Pandas — data cleaning and manipulation  
- NumPy — numerical operations  
- Matplotlib / Plotly — data visualization  

---

# 🧠 System Architecture

The project follows a modular pipeline architecture:

OpenAQ API  
↓  
Data Ingestion  
↓  
Data Cleaning & Preprocessing  
- Missing value handling  
- Outlier detection  
- Sensor noise filtering  
↓  
Data Aggregation  
- Hourly  
- Daily  
- Monthly  
↓  
Visualization Dashboard (Streamlit)

---

# 🧹 Data Processing Pipeline

### 1. Data Ingestion
Air quality data is fetched using the **OpenAQ API**, covering multiple monitoring stations.

### 2. Data Harmonization
Sensor data is standardized to ensure consistency in:

- Units  
- Timestamp formats  
- Reporting frequency  

### 3. Data Cleaning
The cleaning pipeline addresses:

- Missing sensor readings  
- Outliers in pollution measurements  
- Noise in sensor signals  
- Inconsistent or duplicated timestamps  

### 4. Missing Data Strategies

Two different strategies were explored:

1. **Interpolation-based approach**
2. **Model-based imputation**

These methods were compared to understand how data-repair strategies affect environmental interpretation.

---

# 📈 Dashboard Features

The dashboard provides:

### Interactive Visualizations
- Temporal pollution trends  
- Station-wise comparison  
- Pollutant concentration over time  

### Multi-scale Analysis
Data is aggregated across:

- Hourly averages  
- Daily averages  
- Monthly trends  

### Extreme Pollution Events
The system identifies and visualizes:

- Pollution spikes  
- Episode duration  
- Relative intensity across stations  

---

# 🖥️ Running the Dashboard

### Clone the Repository

```bash
git clone https://github.com/yourusername/air-quality-dashboard.git
cd air-quality-dashboard
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Streamlit App

```bash
streamlit run app.py
```

The dashboard will open in your browser.

---

# 📂 Project Structure

```
air-quality-dashboard
│
├── data/                 # Raw and processed datasets
├── api/                  # API fetching scripts
├── cleaning/             # Data cleaning pipeline
├── dashboard/            # Streamlit dashboard
├── utils/                # Helper functions
│
├── app.py                # Main Streamlit application
├── requirements.txt
└── README.md
```

---

# 🔬 Key Insights Explored

- Temporal trends in air pollution levels  
- Spatial variation across monitoring stations  
- Impact of missing-data strategies on environmental analysis  
- Identification of extreme pollution episodes  

---

# ⚠️ Limitations

- Sensor networks may have **calibration drift** over time  
- Data availability varies across monitoring stations  
- Imputation methods can introduce bias in interpretation  
- Some sensors report at irregular time intervals  

These limitations highlight the importance of **careful preprocessing and transparency in environmental analytics.**

---

# 👥 Contributors

| Name | Contribution |
|-----|-------------|
| Ajay Kasaudhan | GUI development and dashboard design |
| Ashik | API integration and data ingestion |
| Hitesh CK | System architecture design |
| Sahil Rajput | Data cleaning and interpolation methods |

---

# 📚 Course Information

This project was completed as a **group project for the Data Science Practices course** at **IISER Pune**.

Instructor: **Prof. Bedarth Goswami**
