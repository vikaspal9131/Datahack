import pandas as pd
from sklearn.preprocessing import LabelEncoder

def load_data(file_path):
    """
    Load the CSV file into a pandas DataFrame.
    
    :param file_path: Path to the CSV file.
    :return: DataFrame containing the sales data.
    """
    return pd.read_csv(file_path)

def handle_missing_values(df):
    """
    Handle missing values by filling in with default values.
    
    :param df: DataFrame with raw sales data.
    :return: DataFrame with missing values handled.
    """
    df.fillna({
        'CGST_Amount': 0,
        'SGST_Amount': 0,
        'VAT_Amount': 0,
        'Service_Charge_Amount': 0,
        'Price': 0,
        'Qty_': 1  # Assuming a default quantity of 1 if not specified
    }, inplace=True)
    return df

def convert_datetime(df):
    """
    Convert 'Date' and 'Timestamp' columns to datetime objects and extract additional features.
    
    :param df: DataFrame containing sales data.
    :return: DataFrame with datetime columns converted and new time features extracted.
    """
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    
    # Extracting useful time-based features
    df['Year'] = df['Timestamp'].dt.year
    df['Month'] = df['Timestamp'].dt.month
    df['Day'] = df['Timestamp'].dt.day
    df['Hour'] = df['Timestamp'].dt.hour
    
    return df

def encode_categorical_data(df):
    """
    Convert categorical columns to numerical data using One-Hot Encoding and Label Encoding.
    
    :param df: DataFrame with raw sales data.
    :return: DataFrame with categorical columns converted to numerical.
    """
    # One-Hot Encoding for 'Payment_Type', 'Order_Type', and 'Area'
    df = pd.get_dummies(df, columns=['Payment_Type', 'Order_Type', 'Area'], drop_first=True)
    
    # Label Encoding for 'Item_Name'
    label_encoder = LabelEncoder()
    df['Item_Name'] = label_encoder.fit_transform(df['Item_Name'])
    
    return df

def create_features(df):
    """
    Create new features such as 'Total_Tax' by combining relevant columns.
    
    :param df: DataFrame with sales data.
    :return: DataFrame with new features added.
    """
    df['Total_Tax'] = df['CGST_Amount'] + df['SGST_Amount'] + df['VAT_Amount']
    return df

def preprocess_sales_data(file_path):
    """
    Perform all preprocessing steps on the sales data.
    
    :param file_path: Path to the CSV file.
    :return: Preprocessed DataFrame ready for machine learning models.
    """
    # Load data
    df = load_data(file_path)
    
    # Handle missing values
    df = handle_missing_values(df)
    
    # Convert datetime columns and extract features
    df = convert_datetime(df)
    
    # Encode categorical data
    df = encode_categorical_data(df)
    
    # Create additional features
    df = create_features(df)
    
    # Drop irrelevant columns (if any)
    df.drop(columns=['Assign_To'], inplace=True, errors='ignore')
    
    return df

# Define the path to the CSV file
csv_path = "Organized/Sales/sales_dump.csv"
output_path = "preprocessed_sales_data.csv"


# Preprocess the data
preprocessed_data = preprocess_sales_data(csv_path)

# Save the preprocessed DataFrame to a new CSV file
preprocessed_data.to_csv(output_path, index=False)
