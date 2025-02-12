import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# Load JSON files with country names and GDP indicators
with open("countries.json", "r") as f:
    country_names = json.load(f)

with open("indicators.json", "r") as f:
    indicators = json.load(f)

# Data folder path
data_folder = "data/base"
season_image_folder = "images/season_decompose"

# Create main subfolders
countries_folder = os.path.join(season_image_folder, "Countries")
indicators_folder = os.path.join(season_image_folder, "Indicators")

os.makedirs(countries_folder, exist_ok=True)
os.makedirs(indicators_folder, exist_ok=True)

# Dictionary to store data for combined seasonal decomposition plots
seasonal_data = {indicator: {} for indicator in indicators}

for country, country_code in country_names.items():
    # Create country-specific folder inside "Countries"
    country_folder = os.path.join(countries_folder, country.replace(' ', '_'))
    os.makedirs(country_folder, exist_ok=True)

    # List to store the plots for the combined figure
    all_plots = []

    for indicator, indicator_code in indicators.items():
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

                # Initialize variables for decomposition results
                result_additive, result_multiplicative = None, None

                # Perform seasonal decomposition (additive and multiplicative)
                try:
                    result_additive = seasonal_decompose(df['Value'], model='additive')
                except ValueError as e:
                    print(f"Could not additive decompose {indicator} for {country}: {e}")

                try:
                    result_multiplicative = seasonal_decompose(df['Value'], model='multiplicative')
                except ValueError as e:
                    print(f"Could not multiplicative decompose {indicator} for {country}: {e}")

                # Create a figure for seasonal decomposition plots
                fig, axes = plt.subplots(2, 4, figsize=(20, 10))

                # Set the overall figure title
                fig.suptitle(f"Seasonal Decomposition for {country}, {indicator}", fontsize=24)

                # Plot Additive decomposition if successful
                if result_additive:
                    axes[0, 0].plot(result_additive.observed)
                    axes[0, 0].set_title(f"Additive: Observed")

                    axes[0, 1].plot(result_additive.trend)
                    axes[0, 1].set_title(f"Additive: Trend")

                    axes[0, 2].plot(result_additive.seasonal)
                    axes[0, 2].set_title(f"Additive: Seasonal")

                    axes[0, 3].plot(result_additive.resid)
                    axes[0, 3].set_title(f"Additive: Residual")
                else:
                    for ax in axes[0]:
                        ax.axis('off')  # Clear axes if decomposition fails

                # Plot Multiplicative decomposition if successful
                if result_multiplicative:
                    axes[1, 0].plot(result_multiplicative.observed)
                    axes[1, 0].set_title(f"Multiplicative: Observed")

                    axes[1, 1].plot(result_multiplicative.trend)
                    axes[1, 1].set_title(f"Multiplicative: Trend")

                    axes[1, 2].plot(result_multiplicative.seasonal)
                    axes[1, 2].set_title(f"Multiplicative: Seasonal")

                    axes[1, 3].plot(result_multiplicative.resid)
                    axes[1, 3].set_title(f"Multiplicative: Residual")
                else:
                    for ax in axes[1]:
                        ax.axis('off')  # Clear axes if decomposition fails

                plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust layout to accommodate the figure title

                # Save the seasonal decomposition plots in the country folder
                country_image_path = os.path.join(country_folder, f"Seasonality_{country.replace(' ', '_')}_{indicator.replace(' ', '_')}.png")
                plt.savefig(country_image_path)

                # Create indicator-specific folder inside "Indicators"
                indicator_folder = os.path.join(indicators_folder, indicator.replace(' ', '_'))
                os.makedirs(indicator_folder, exist_ok=True)

                # Save the seasonal decomposition plots in the indicator folder
                indicator_image_path = os.path.join(indicator_folder, f"Seasonality_{country.replace(' ', '_')}_{indicator.replace(' ', '_')}.png")
                plt.savefig(indicator_image_path)

                plt.close()
                print(f"Saved: {country_image_path}")
                print(f"Saved: {indicator_image_path}")

                # Store the plot for the combined figure
                all_plots.append((country, indicator, country_image_path))

                # Store data for combined seasonal decomposition plots
                seasonal_data[indicator][country] = df['Value']

    # Create a combined figure for all indicators for the current country
    fig_combined, axes_combined = plt.subplots(len(all_plots), 1, figsize=(10, 5 * len(all_plots)))

    # Plot each indicator's decomposition in the combined figure
    for i, (country, indicator, image_path) in enumerate(all_plots):
        axes_combined[i].imshow(plt.imread(image_path))  # Use the saved image for each plot
        axes_combined[i].axis('off')  # Turn off axis for clean look


    # Save the combined image for the country
    combined_image_path = os.path.join(country_folder, f"Seasonality_All_Indicators_{country.replace(' ', '_')}.png")
    plt.tight_layout()
    plt.savefig(combined_image_path)
    plt.close()

    print(f"Saved combined image: {combined_image_path}")

# Generate and save combined seasonal decomposition plots for each indicator
for indicator, country_series in seasonal_data.items():
    if country_series:
        # Create a vertical stack of subplots (one per country)
        num_countries = len(country_series)
        fig, axes = plt.subplots(num_countries, 1, figsize=(10, 5 * num_countries))  # Stack vertically
        
        # If only one country, axes is not an array, so we handle that case
        if num_countries == 1:
            axes = [axes]
        
        for i, (country, series) in enumerate(country_series.items()):
            # Plot the seasonal decomposition for each country in its subplot
            # This assumes the plot images already exist
            axes[i].imshow(plt.imread(f"images/season_decompose/Countries/{country.replace(' ', '_')}/Seasonality_{country.replace(' ', '_')}_{indicator.replace(' ', '_')}.png"))
            axes[i].axis('off')  # Turn off axis for clean look


        # Adjust layout for better spacing
        plt.tight_layout()

        # Save combined seasonal decomposition image inside "Indicators"
        combined_seasonal_image_path = os.path.join(indicators_folder, indicator.replace(' ', '_'), f"Seasonality_All_Countries_{indicator.replace(' ', '_')}.png")
        plt.savefig(combined_seasonal_image_path)
        plt.close()
        print(f"Saved: {combined_seasonal_image_path}")
