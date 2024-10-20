# basicTraining.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from zenml.steps import step

def train_model(data: pd.DataFrame) -> pd.DataFrame:
    """Train an ARIMA model and return predictions.

    Args:
        data (pd.DataFrame): Preprocessed sales data.

    Returns:
        pd.DataFrame: DataFrame containing actual and predicted sales.
    """
    # Set date as index
    data.set_index('Date', inplace=True)

    # Aggregate daily sales
    daily_sales = data.resample('D').sum()

    # Check for stationarity
    result = adfuller(daily_sales['Order_Total'])
    if result[1] > 0.05:  # Non-stationary
        daily_sales['Order_Total'] = daily_sales['Order_Total'].diff().dropna()

    # Split into training and test sets
    train_size = int(len(daily_sales) * 0.8)
    train, test = daily_sales[:train_size], daily_sales[train_size:]

    # Fit ARIMA model
    model = ARIMA(train['Order_Total'], order=(5, 1, 0))  # Adjust order based on ACF/PACF plots
    model_fit = model.fit()

    # Make predictions
    predictions = model_fit.forecast(steps=len(test))
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

    return test[['Order_Total', 'Predicted']]

# Wrap the function with the ZenML step decorator
train_model = step(train_model)
