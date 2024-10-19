# Importing necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

# To avoid warnings with dates
register_matplotlib_converters()

# Load the final dataset
data_path = '../prepared/final_data.csv'
df = pd.read_csv(data_path)

# Display basic information about the dataset
print("Dataset Information:")
print(df.info())
print("\nFirst 5 rows of the dataset:")
print(df.head())

# Data Preprocessing
# Convert 'Date' to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Basic statistics
print("\nBasic Statistics:")
print(df.describe())

# Exploratory Data Analysis (EDA)

## 1. Sales Over Time
plt.figure(figsize=(14, 7))
df.groupby('Date')['Order_Total'].sum().plot()
plt.title('Total Sales Over Time')
plt.xlabel('Date')
plt.ylabel('Total Sales')
plt.grid()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

## 2. Sales Distribution
plt.figure(figsize=(14, 7))
sns.histplot(df['Order_Total'], bins=30, kde=True)
plt.title('Sales Distribution')
plt.xlabel('Order Total')
plt.ylabel('Frequency')
plt.grid()
plt.tight_layout()
plt.show()

## 3. Sales by Payment Type
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='Payment_Type', y='Order_Total', estimator=sum)
plt.title('Total Sales by Payment Type')
plt.xlabel('Payment Type')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()
plt.show()

## 4. Sales by Order Type
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='Order_Type', y='Order_Total', estimator=sum)
plt.title('Total Sales by Order Type')
plt.xlabel('Order Type')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()
plt.show()

## 5. Monthly Sales Trend
df['Month'] = df['Date'].dt.to_period('M')
monthly_sales = df.groupby('Month')['Order_Total'].sum().reset_index()
monthly_sales['Month'] = monthly_sales['Month'].dt.to_timestamp()

plt.figure(figsize=(14, 7))
plt.plot(monthly_sales['Month'], monthly_sales['Order_Total'], marker='o')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()
plt.show()

## 6. Heatmap for Daily Sales
# First, group the data by date and order type to get total sales
daily_sales = df.groupby(['Date', 'Order_Type'])['Order_Total'].sum().reset_index()

# Now, pivot the daily_sales DataFrame for the heatmap
daily_sales_pivot = daily_sales.pivot(index='Date', columns='Order_Type', values='Order_Total').fillna(0)

# Plotting the heatmap
plt.figure(figsize=(14, 7))
sns.heatmap(daily_sales_pivot, cmap='YlGnBu', annot=True, fmt='.1f')
plt.title('Heatmap of Daily Sales by Order Type')
plt.xlabel('Order Type')
plt.ylabel('Date')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

## 7. Correlation Matrix
plt.figure(figsize=(8, 6))

# Selecting only numeric columns for correlation
numeric_df = df.select_dtypes(include=['float64', 'int64'])  # Select numeric types only
correlation_matrix = numeric_df.corr()

sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix')
plt.tight_layout()
plt.show()