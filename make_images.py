import os
import json
import pandas as pd
import matplotlib.pyplot as plt

# Load JSON files with country names and GDP indicators
with open("countries.json", "r") as f:
    country_names = json.load(f)

with open("indicators.json", "r") as f:
    indicators = json.load(f)

# Data folder path
data_folder = "data"
image_folder = "images"
os.makedirs(image_folder, exist_ok=True)

# Iterate over country and indicator combinations
for country, country_code in country_names.items():
    for indicator, indicator_code in indicators.items():
        # Create the expected filename format
        filename = f"{country.replace(' ', '_')}_{indicator.replace(' ', '_')}.parquet"
        filepath = os.path.join(data_folder, filename)
        
        if os.path.exists(filepath):
            # Load the Parquet file
            df = pd.read_parquet(filepath)
            
            # Ensure the DataFrame has a date column
            if 'Value' in df.columns:
                df = df.set_index('Year')
                
                # Plot the data
                plt.figure(figsize=(10, 5))
                plt.plot(df['Value'], marker='o', linestyle='-')
                plt.xlabel("Date")
                plt.ylabel(indicator)
                plt.title(f"{indicator} in {country}")
                plt.xticks(rotation=45)
                plt.grid()
                
                # Save the figure
                image_path = os.path.join(image_folder, f"{country.replace(' ', '_')}_{indicator.replace(' ', '_')}.png")
                plt.savefig(image_path)
                plt.close()
                
                print(f"Saved: {image_path}")
