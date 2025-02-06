import os
import json
import requests
import pandas as pd

# Load countries and indicators from JSON files
with open("countries.json", "r") as f:
    countries = json.load(f)

with open("indicators.json", "r") as f:
    indicators = json.load(f)

# Define the API URL and parameters
base_url = "http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}"
params = {"format": "json", "per_page": 10000}

# Folder to store parquet files
output_folder = "data"
os.makedirs(output_folder, exist_ok=True)

# Fetch and save data
for country_name, country_code in countries.items():
    print(f"Fetching data for {country_name}...")
    
    country_data = []

    for indicator_name, indicator_code in indicators.items():
        response = requests.get(base_url.format(country_code=country_code, indicator_code=indicator_code), params=params)
        
        if response.status_code == 200:
            data = response.json()
            indicator_data = []
            
            if data and len(data) > 1:
                for entry in data[1]:
                    if "value" in entry and "date" in entry:
                        record = {
                            "Year": int(entry["date"]),
                            "Indicator": indicator_name,
                            "Value": entry["value"]
                        }
                        country_data.append(record)
                        indicator_data.append(record)

            if indicator_data:
                df_indicator = pd.DataFrame(indicator_data).sort_values(by="Year")
                file_name = f"{country_name.replace(' ', '_')}_{indicator_name.replace(' ', '_')}.parquet"
                file_path = os.path.join(output_folder, file_name)
                df_indicator.to_parquet(file_path, index=False)
                print(f"Saved {file_path}")

        else:
            print(f"Failed to fetch {indicator_name} for {country_name}")

    if country_data:
        df_country = pd.DataFrame(country_data).pivot(index="Year", columns="Indicator", values="Value").reset_index()
        file_path = os.path.join(output_folder, f"{country_name.replace(' ', '_')}.parquet")
        df_country.to_parquet(file_path, index=False)
        print(f"Saved {file_path}")

print("Data collection complete.")
