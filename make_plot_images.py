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
data_folder = "data/base"
base_image_folder = "images/plot"

# Create main subfolders
countries_folder = os.path.join(base_image_folder, "Countries")
indicators_folder = os.path.join(base_image_folder, "Indicators")

os.makedirs(countries_folder, exist_ok=True)
os.makedirs(indicators_folder, exist_ok=True)

# Dictionary to store data for combined indicator plots
indicator_data = {indicator: {} for indicator in indicators}

# Iterate over country and indicator combinations
for country, country_code in country_names.items():
    # Create country-specific folder inside "Countries"
    country_folder = os.path.join(countries_folder, country.replace(' ', '_'))
    os.makedirs(country_folder, exist_ok=True)

    fig, axes = plt.subplots(len(indicators), 1, figsize=(10, 5 * len(indicators)))
    
    for i, (indicator, indicator_code) in enumerate(indicators.items()):
        # Create the expected filename format
        filename = f"{country.replace(' ', '_')}_{indicator.replace(' ', '_')}.parquet"
        filepath = os.path.join(data_folder, filename)
        
        if os.path.exists(filepath):
            # Load the Parquet file
            df = pd.read_parquet(filepath)
            
            # Ensure the DataFrame has a date column
            if 'Year' in df.columns and 'Value' in df.columns:
                df = df.set_index('Year')

                # Plot individual image
                plt.figure(figsize=(10, 5))
                plt.plot(df['Value'], marker='o', linestyle='-')
                plt.xlabel("Date")
                plt.ylabel(indicator)
                plt.title(f"{indicator} in {country}")
                plt.xticks(rotation=45)
                plt.grid()
                
                # Create indicator-specific folder inside "Indicators"
                indicator_folder = os.path.join(indicators_folder, indicator.replace(' ', '_'))
                os.makedirs(indicator_folder, exist_ok=True)

                # Save individual figure in country folder inside "Countries"
                country_image_path = os.path.join(country_folder, f"Line_{country.replace(' ', '_')}_{indicator.replace(' ', '_')}.png")
                plt.savefig(country_image_path)

                # Save individual figure in indicator folder inside "Indicators"
                indicator_image_path = os.path.join(indicator_folder, f"Line_{country.replace(' ', '_')}_{indicator.replace(' ', '_')}.png")
                plt.savefig(indicator_image_path)

                plt.close()
                print(f"Saved: {country_image_path}")
                print(f"Saved: {indicator_image_path}")
                
                # Add to combined figure for the country
                axes[i].plot(df['Value'], marker='o', linestyle='-', label=country)
                axes[i].set_xlabel("Date")
                axes[i].set_ylabel(indicator)
                axes[i].set_title(f"{indicator} in {country}")
                axes[i].grid()

                # Store data for combined indicator plots
                indicator_data[indicator][country] = df['Value']
    
    # Save the combined image for the country
    combined_image_path = os.path.join(country_folder, f"Line_{country.replace(' ', '_')}_all_indicators.png")
    plt.tight_layout()
    plt.savefig(combined_image_path)
    plt.close()
    print(f"Saved: {combined_image_path}")

# Generate and save combined plots for each indicator
for indicator, country_series in indicator_data.items():
    if country_series:
        plt.figure(figsize=(10, 5))
        
        for country, series in country_series.items():
            plt.plot(series, marker='o', linestyle='-', label=country)

        plt.xlabel("Date")
        plt.ylabel(indicator)
        plt.title(f"{indicator} across all countries")
        plt.xticks(rotation=45)
        plt.grid()
        plt.legend()

        # Save combined indicator image inside "Indicators"
        combined_indicator_image_path = os.path.join(indicators_folder, indicator.replace(' ', '_'), f"Line_All_Countries_{indicator.replace(' ', '_')}.png")
        plt.savefig(combined_indicator_image_path)
        plt.close()
        print(f"Saved: {combined_indicator_image_path}")