# Project Title

A brief description of your project, its purpose, and what it does.

## Table of Contents
- [Usage](#usage)
  - [Data Collection](#data-collection)
  - [Visualization](#visualization)
  - [Model Training](#model-training)

- [Images](#images)
  - [Plot graph](#plot)
  - [Prediction plot graphs](#model_plot)

## Overview
This project gathers economic and financial data from the World Bank API, visualizes key indicators across different countries, and trains machine learning models to analyze trends and make predictions.



## Usage
### Data Collection
Run `get_data.py` to fetch data from the World Bank API:
```bash
python get_data.py
```
This script retrieves and stores relevant economic indicators for selected countries.

### Visualization
Run `make_images.py` to generate graphs for all indicator-country combinations:
```bash
python make_images.py
```
The script produces visualizations that help in understanding trends and correlations.

### Model Training
Open `model_training.ipynb` in Jupyter Notebook and execute the cells to:
- Train multiple machine learning models
- Perform model selection based on evaluation metrics
- Visualize the best-performing models

## Images

### Plot graph
- Whole dataset in plot graph

### Prediction plot graphs
- Plot graphs of predicted vs actual values




## Dependencies
In requirements.txt



