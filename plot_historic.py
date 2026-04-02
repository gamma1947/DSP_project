import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# Set your extreme threshold here
EXTREME_THRESHOLD = 35.0  

def load_and_clean_data(filepath):
    print("Loading and cleaning data...")
    df = pd.read_csv(filepath)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)
    
    # Clean and interpolate
    df[df < 0] = np.nan
    missing_percentages = df.isnull().mean() * 100
    valid_sensors = missing_percentages[missing_percentages <= 60].index
    df_clean = df[valid_sensors].copy()
    df_clean = df_clean.interpolate(method='time', limit=12)
    
    # Resample to Daily Averages
    daily_df = df_clean.resample('1D').mean()
    return daily_df

def plot_sensor_bar_chart():
    daily_df = load_and_clean_data('o3 (1).csv')
    delhi_avg = daily_df.mean(axis=1)
    
    # Define the colormap (Yellow -> Orange -> Red)
    cmap = plt.get_cmap('YlOrRd')
    
    while True:
        sensor_id = input(f"\nEnter the Location ID to plot (or 'exit' to quit): ").strip()
        
        if sensor_id.lower() == 'exit':
            print("Exiting program.")
            break
            
        if sensor_id not in daily_df.columns:
            print(f"Error: Sensor ID '{sensor_id}' not found. Please try another.")
            continue
            
        # Extract specific sensor data
        data_series = daily_df[sensor_id]
        
        # Create a normalizer based on the specific sensor's min and max
        norm = mcolors.Normalize(vmin=data_series.min(), vmax=data_series.max())
        
        plt.figure(figsize=(14, 6))
        
        # 1. Plot the bars
        bars = plt.bar(daily_df.index, data_series, width=0.8, edgecolor='black', linewidth=0.5)
        
        # 2. Color each bar dynamically
        for bar, val in zip(bars, data_series):
            if not pd.isna(val):
                # Set color based on value
                bar.set_color(cmap(norm(val)))
                bar.set_edgecolor('black') # Keep the black outline
                
                # Add diagonal lines if it crosses the extreme threshold
                if val >= EXTREME_THRESHOLD:
                    bar.set_hatch('//')

        # 3. Draw Threshold and City Average
        plt.axhline(y=EXTREME_THRESHOLD, color='darkred', linestyle='-', linewidth=2, 
                    label=f'Extreme Threshold ({EXTREME_THRESHOLD})')
        plt.plot(daily_df.index, delhi_avg, color='blue', linewidth=2, linestyle='--', 
                 label='Delhi Overall Average')
        
        # 4. Add the Colorbar legend
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([]) 
        cbar = plt.colorbar(sm, ax=plt.gca(), pad=0.02)
        cbar.set_label('O3 Concentration', rotation=270, labelpad=15)
        
        # 5. Text and Layout
        plt.title(f'Daily Average O3 Levels - Sensor {sensor_id}\n(Colored by Intensity, Hatched = Extreme)', pad=10)
        plt.xlabel('Date')
        plt.ylabel('O3 Pollutant Level')
        plt.legend(loc='upper right')
        plt.grid(axis='y', linestyle=':', alpha=0.6)
        
        plt.tight_layout()
        plt.show()

# Run it
if __name__ == "__main__":
    plot_sensor_bar_chart()