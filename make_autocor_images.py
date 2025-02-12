import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import autocorrelation_plot

# Load JSON files with country names and GDP indicators
with open("countries.json", "r") as f:
    country_names = json.load(f)

with open("indicators.json", "r") as f:
    indicators = json.load(f)

# Data folder path
data_folder = "data/base"
autocor_image_folder = "images/autocor_plot"

# Create main subfolders
countries_folder = os.path.join(autocor_image_folder, "Countries")
indicators_folder = os.path.join(autocor_image_folder, "Indicators")

os.makedirs(countries_folder, exist_ok=True)
os.makedirs(indicators_folder, exist_ok=True)

# Dictionary to store data for combined autocorrelation plots
autocor_data = {indicator: {} for indicator in indicators}

for country, country_code in country_names.items():
    # Create country-specific folder inside "Countries"
    country_folder = os.path.join(countries_folder, country.replace(' ', '_'))
    os.makedirs(country_folder, exist_ok=True)

    # Create a figure for the combined autocorrelation plots
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
                df.index = pd.to_datetime(df.index, format='%Y')
                df = df.dropna()

                # Plot the autocorrelation plot for individual image
                plt.figure(figsize=(10, 5))
                autocorrelation_plot(df['Value'])
                plt.title(f"Autocorrelation of {indicator} in {country}")

                # Save individual autocorrelation plot in country folder inside "Countries"
                country_image_path = os.path.join(country_folder, f"Autocor_{country.replace(' ', '_')}_{indicator.replace(' ', '_')}.png")
                plt.savefig(country_image_path)

                # Create indicator-specific folder inside "Indicators"
                indicator_folder = os.path.join(indicators_folder, indicator.replace(' ', '_'))
                os.makedirs(indicator_folder, exist_ok=True)

                # Save individual autocorrelation plot in indicator folder inside "Indicators"
                indicator_image_path = os.path.join(indicator_folder, f"Autocor_{country.replace(' ', '_')}_{indicator.replace(' ', '_')}.png")
                plt.savefig(indicator_image_path)

                plt.close()
                print(f"Saved: {country_image_path}")
                print(f"Saved: {indicator_image_path}")
                
                # Store data for combined autocorrelation plots
                autocor_data[indicator][country] = df['Value']

                # Plot the autocorrelation plot for the combined figure (all indicators in one figure)
                if len(indicators) == 1:
                    autocorrelation_plot(df['Value'], ax=axes)
                    axes.set_title(f"Autocorrelation of {indicator} in {country}")
                else:
                    autocorrelation_plot(df['Value'], ax=axes[i])  # Plot each indicator in a separate subplot
                    axes[i].set_title(f"Autocorrelation of {indicator} in {country}")
                    axes[i].legend([country], loc='best')  # Add legend for the country

    # Save the combined autocorrelation image for the country
    combined_autocor_image_path = os.path.join(country_folder, f"Autocor_{country.replace(' ', '_')}_all_indicators.png")
    plt.tight_layout()
    plt.savefig(combined_autocor_image_path)
    plt.close()
    print(f"Saved: {combined_autocor_image_path}")

# Generate and save combined autocorrelation plots for each indicator
for indicator, country_series in autocor_data.items():
    if country_series:
        # Create a vertical stack of subplots (one per country)
        num_countries = len(country_series)
        fig, axes = plt.subplots(num_countries, 1, figsize=(10, 5 * num_countries))  # Stack vertically
        
        # If only one country, axes is not an array, so we handle that case
        if num_countries == 1:
            axes = [axes]
        
        for i, (country, series) in enumerate(country_series.items()):
            # Plot the autocorrelation for each country in its subplot
            autocorrelation_plot(series, ax=axes[i])
            axes[i].set_title(f"Autocorrelation of {indicator} in {country}")
            axes[i].legend([country], loc='best')  # Add legend for each country

        # Adjust layout for better spacing
        plt.tight_layout()

        # Save combined autocorrelation image inside "Indicators"
        combined_autocor_indicator_image_path = os.path.join(indicators_folder, indicator.replace(' ', '_'), f"Autocor_All_Countries_{indicator.replace(' ', '_')}.png")
        plt.savefig(combined_autocor_indicator_image_path)
        plt.close()
        print(f"Saved: {combined_autocor_indicator_image_path}")

