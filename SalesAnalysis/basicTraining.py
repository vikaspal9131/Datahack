import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

# Load the merged data
data_path = '../prepared/final_data.csv'
sales_data = pd.read_csv(data_path)

# Convert the 'Date' column to datetime
sales_data['Date'] = pd.to_datetime(sales_data['Date'])
sales_data.set_index('Date', inplace=True)

# Ensure 'Order_Total' is numeric
sales_data['Order_Total'] = pd.to_numeric(sales_data['Order_Total'], errors='coerce')

# Drop any rows with NaN values (if any)
sales_data.dropna(subset=['Order_Total'], inplace=True)

# Aggregate sales data by day
daily_sales = sales_data.resample('D').sum()

# Visualize the time series data
plt.figure(figsize=(12, 6))
plt.plot(daily_sales['Order_Total'], label='Daily Sales', color='blue')
plt.title('Daily Sales Over Time')
plt.xlabel('Date')
plt.ylabel('Order Total')
plt.legend()
plt.show()

# Check for stationarity using the Augmented Dickey-Fuller test
result = adfuller(daily_sales['Order_Total'])
print(f'ADF Statistic: {result[0]}')
print(f'p-value: {result[1]}')

# If p-value > 0.05, the series is non-stationary; apply differencing
if result[1] > 0.05:
    daily_sales['Order_Total'] = daily_sales['Order_Total'].diff().dropna()

# Split the data into training and testing sets
train_size = int(len(daily_sales) * 0.8)
train, test = daily_sales[:train_size], daily_sales[train_size:]

# Fit the ARIMA model
model = ARIMA(train['Order_Total'], order=(5, 1, 0))  # Adjust order based on ACF/PACF plots
model_fit = model.fit()

# Make predictions
predictions = model_fit.forecast(steps=len(test))

# Create a DataFrame for test set predictions
test = pd.DataFrame(test)  # Convert test to DataFrame for adding predictions
test['Predicted'] = predictions

# Plot results
plt.figure(figsize=(12, 6))
plt.plot(train['Order_Total'], label='Training Data', color='blue')
plt.plot(test['Order_Total'], label='Actual Sales', color='green')
plt.plot(test['Predicted'], label='Predicted Sales', color='red')
plt.title('Sales Forecasting using ARIMA')
plt.xlabel('Date')
plt.ylabel('Order Total')
plt.legend()
plt.show()

# Print predictions
print(test[['Order_Total', 'Predicted']])
