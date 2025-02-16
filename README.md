# Time Series Forecasting Project

This project focuses on forecasting time series data for various indicators across countries. We use different machine learning models such as Prophet, XGBoost, LSTM, ARIMA, and Exponential Smoothing to train on the data. The project organizes the components in several files and folders for better workflow management.

## Project Structure

### 1. **`models.ipynb`**  
This is the main file where we load the best parameters for each model, apply those parameters to the datasets, and create final dataframes with aggregated results. The resulting dataframes are stored in the `data` folder.

### 2. **`get_data.py`**  
A Python script responsible for gathering and preparing the input data for each indicator-country combination. This script creates the dataset in a format suitable for training the models.

### 3. **`model_ipynb` Folder**  
This folder contains Jupyter notebooks for training individual models on the data. For now, the folder includes the following models:
   - **Prophet**
   - **XGBoost**
   - **LSTM**
   - **Exponential Smoothing**
   - **ARIMA**  

Each model is trained and evaluated in separate notebooks within this folder.

### 4. **`make_images` Folder**  
This folder contains scripts for generating basic visualizations from the data. Visualizations include plots like the time series data, model predictions, and error rates across different models.

### 5. **`best_params` Folder**  
This folder holds JSON files containing the best parameters for each of the models. Each parameter set is specific to the combination of country and indicator being forecasted.

### 6. **`data` Folder**  
The `data` folder contains:
   - **Input data**: Raw time series data for various indicators and countries.
   - **Output dataframes**: DataFrames containing the final aggregated results after model predictions are made. These dataframes are the results of training and testing the models on the datasets.

### 7. **`images` Folder**  
This folder contains all of the visualizations generated from the data. These include model performance, error metrics, and prediction visuals.


## Dependencies
In requirements.txt



