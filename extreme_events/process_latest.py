import pandas as pd
import os

# Set your input file path here
input_file_path = r'data_latest\o3_latest_india.csv'

# Extract the pollutant name from the file path
# 1. os.path.basename gets 'o3_latest_india.csv' from the full path
# 2. .split('_')[0] splits it by underscores and grabs the very first item ('o3')
filename = os.path.basename(input_file_path)
pollutant_name = filename.split('_')[0]
print(f"Detected pollutant: {pollutant_name}")

# 1. Load the CSV file
df = pd.read_csv(input_file_path)

# Count the number of unique entries in the location_id column
unique_location_ids = df['location_id'].nunique()

# Get the total number of entries (rows) in the CSV
total_entries = len(df)

# Check if they are equal
is_equal = unique_location_ids == total_entries

print(f"Number of unique location IDs: {unique_location_ids}")
print(f"Total number of entries (rows) in the CSV: {total_entries}")
print(f"Are they equal? {is_equal}")

# 2. Convert UTC timestamps to datetime objects and drop local time
df['datetime_utc'] = pd.to_datetime(df['datetime_utc'])
df.drop(columns=['datetime_local'], inplace=True)

# 3. Sort by sensor_id and time sequentially 
df = df.sort_values(by=['sensor_id', 'datetime_utc'])

# 4. Set the timestamp as the index (required for time resampling)
df.set_index('datetime_utc', inplace=True)

# 5. Group by sensor_id and apply 1-Hour resampling, taking the mean of the values
agg_cols = ['value', 'lat', 'lon', 'location_id']
df_hourly = df.groupby('sensor_id')[agg_cols].resample('1h').mean().reset_index()

# 6. Clean up Location ID format (ensure it stays as an Integer)
df_hourly['location_id'] = df_hourly['location_id'].round().astype(pd.Int64Dtype())

# 7. Save output dynamically
output_filename = f'hourly_resampled_{pollutant_name}.csv'
df_hourly.to_csv(output_filename, index=False)
print(f"Resampled data successfully saved as {output_filename}!")