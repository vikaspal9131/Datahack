# EDA.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from zenml.steps import step, Output

@step
def perform_eda(data: pd.DataFrame) -> None:
    """Perform Exploratory Data Analysis on the provided data."""
    # EDA Code
    # Display basic information about the dataset
    print("Dataset Information:")
    print(data.info())
    print("\nFirst 5 rows of the dataset:")
    print(data.head())

    # ... (rest of your EDA code)

    # Example plot
    plt.figure(figsize=(14, 7))
    data.groupby('Date')['Order_Total'].sum().plot()
    plt.title('Total Sales Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Sales')
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
