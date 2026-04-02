import pandas as pd
import os

# 1. Put the paths to your 3 different files here
file_paths = [
    r'data_latest\o3_latest_india.csv',
    r'data_latest\pm25_latest_india.csv',  # Replace with your actual file name
    r'data_latest\no2_latest_india.csv'    # Replace with your actual file name
]

# Loop through each file in the list
for input_file_path in file_paths:
    try:
        # Extract the pollutant name from the file path
        filename = os.path.basename(input_file_path)
        pollutant_name = filename.split('_')[0]
        
        print(f" Processing: {pollutant_name.upper()} ")
        
        # Load the CSV file
        df = pd.read_csv(input_file_path)

        # Convert UTC timestamps to datetime objects 
        df['datetime_utc'] = pd.to_datetime(df['datetime_utc'])
        
        # Drop local time if it exists in the file
        if 'datetime_local' in df.columns:
            df.drop(columns=['datetime_local'], inplace=True)

        # Sort by sensor_id and time sequentially 
        df = df.sort_values(by=['sensor_id', 'datetime_utc'])

        # Set the timestamp as the index
        df.set_index('datetime_utc', inplace=True)

        # Group by sensor_id and apply 1-Hour resampling
        agg_cols = ['value', 'lat', 'lon', 'location_id']
        
        # Ensure the columns actually exist before resampling (to avoid errors)
        valid_agg_cols = [col for col in agg_cols if col in df.columns]
        df_hourly = df.groupby('sensor_id')[valid_agg_cols].resample('1h').mean().reset_index()

        # Clean up Location ID format (ensure it stays as an Integer)
        if 'location_id' in df_hourly.columns:
            df_hourly['location_id'] = df_hourly['location_id'].round().astype(pd.Int64Dtype())

        # Verification metrics
        unique_location_ids = df_hourly['location_id'].nunique()
        total_entries = len(df_hourly)
        
        print(f"Unique location IDs: {unique_location_ids}")
        print(f"Total rows in output: {total_entries}")
        print(f"Location IDs == Total Rows? {unique_location_ids == total_entries}")

        # Save output dynamically for this specific pollutant
        output_filename = f'hourly_resampled_{pollutant_name}.csv'
        df_hourly.to_csv(output_filename, index=False)
        
        print(f"Success: Data saved as '{output_filename}'")

    except FileNotFoundError:
        print(f"Error: Could not find the file at {input_file_path}")
    except Exception as e:
        print(f"An error occurred with {filename}: {e}")

print("All files processed!")