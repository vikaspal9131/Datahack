import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet
import xgboost as xgb
from sklearn.metrics import mean_squared_error

# Load the data
data = pd.read_csv('../prepared/final_data.csv', parse_dates=['Date'])
data.set_index('Date', inplace=True)

# Check for NaN values in the dataset
if data.isnull().values.any():
    print("NaN values detected in the dataset. Filling NaNs with forward fill.")
    data.fillna(method='ffill', inplace=True)  # Forward fill or use another method to handle NaNs

# Prepare the dataset for Prophet
prophet_data = data.reset_index()[['Date', 'Order_Total']]
prophet_data.columns = ['ds', 'y']

# Define the forecast horizon
forecast_horizon = 7  # Forecasting 7 days ahead

# Function to evaluate model performance
def evaluate_model(y_true, y_pred, model_name):
    mse = mean_squared_error(y_true, y_pred)
    print(f'{model_name} MSE: {mse:.2f}')

# Initialize storage for results
results = {}

# 1. Prophet Model
prophet_model = Prophet()
prophet_model.fit(prophet_data)

future = prophet_model.make_future_dataframe(periods=forecast_horizon)
forecast_prophet = prophet_model.predict(future)
y_true_prophet = data['Order_Total'][-forecast_horizon:].values
y_pred_prophet = forecast_prophet['yhat'][-forecast_horizon:].values

# Check for NaN in Prophet predictions
if np.isnan(y_pred_prophet).any():
    print("NaN values detected in Prophet predictions. Filling NaNs with zero.")
    y_pred_prophet = np.nan_to_num(y_pred_prophet)

evaluate_model(y_true_prophet, y_pred_prophet, 'Prophet')
results['Prophet'] = y_pred_prophet

# 2. ARIMA Model
arima_model = ARIMA(data['Order_Total'], order=(5, 1, 0))
arima_model_fit = arima_model.fit()
y_pred_arima = arima_model_fit.forecast(steps=forecast_horizon)

# Check for NaN in ARIMA predictions
if np.isnan(y_pred_arima).any():
    print("NaN values detected in ARIMA predictions. Filling NaNs with zero.")
    y_pred_arima = np.nan_to_num(y_pred_arima)

evaluate_model(y_true_prophet, y_pred_arima, 'ARIMA')
results['ARIMA'] = y_pred_arima

# 3. XGBoost Model
# Preparing the data for XGBoost
data['lag_1'] = data['Order_Total'].shift(1)
data['lag_2'] = data['Order_Total'].shift(2)
data['lag_3'] = data['Order_Total'].shift(3)
data.dropna(inplace=True)

X = data[['lag_1', 'lag_2', 'lag_3']]
y = data['Order_Total']
X_train, y_train = X[:-forecast_horizon], y[:-forecast_horizon]
X_test, y_test = X[-forecast_horizon:], y[-forecast_horizon:]

# Train XGBoost model
xgb_model = xgb.XGBRegressor()
xgb_model.fit(X_train, y_train)

# Make predictions
y_pred_xgb = xgb_model.predict(X_test)

# Check for NaN in XGBoost predictions
if np.isnan(y_pred_xgb).any():
    print("NaN values detected in XGBoost predictions. Filling NaNs with zero.")
    y_pred_xgb = np.nan_to_num(y_pred_xgb)

evaluate_model(y_test, y_pred_xgb, 'XGBoost')
results['XGBoost'] = y_pred_xgb

# Plotting the predictions
plt.figure(figsize=(14, 7))
plt.plot(data.index[-forecast_horizon:], y_true_prophet, label='True Values', marker='o')
plt.plot(data.index[-forecast_horizon:], y_pred_prophet, label='Prophet Predictions', marker='o')
plt.plot(data.index[-forecast_horizon:], y_pred_arima, label='ARIMA Predictions', marker='o')
plt.plot(data.index[-forecast_horizon:], y_pred_xgb, label='XGBoost Predictions', marker='o')
plt.title('Model Predictions vs True Values')
plt.xlabel('Date')
plt.ylabel('Order Total')
plt.legend()
plt.show()

# Display results
results_df = pd.DataFrame(results, index=data.index[-forecast_horizon:])
print(results_df)
