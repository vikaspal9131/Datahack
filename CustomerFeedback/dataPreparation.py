import pandas as pd

# Load the datasets
food_feedback = pd.read_csv('../Raw/food_feedback_dump.csv')
service_feedback = pd.read_csv('../Raw/service_feedback_dump.csv')

# Inspect the first few rows of each dataset
print("Food Feedback Data:")
print(food_feedback.head())
print("\nService Feedback Data:")
print(service_feedback.head())

# Check for missing values in both datasets
print("\nMissing Values in Food Feedback:")
print(food_feedback.isnull().sum())
print("\nMissing Values in Service Feedback:")
print(service_feedback.isnull().sum())

# Handle missing values (example: filling missing values with 'Unknown' for categorical fields)
food_feedback.fillna({
    'Customer_Name_ff': 'Unknown',
    'From__ff': 'Unknown',
    'Customer_Email_ff': 'Unknown',
    'Invoice_Id_ff': 'Unknown',
    'Table_No_ff': 'Unknown',
    'Order_Type_ff': 'Unknown',
    'Answer_ff': 'No Feedback',
}, inplace=True)

service_feedback.fillna({
    'Customer_Name_sf': 'Unknown',
    'From__sf': 'Unknown',
    'Customer_Email_sf': 'Unknown',
    'Invoice_Id_sf': 'Unknown',
    'Table_No_sf': 'Unknown',
    'Order_Type_sf': 'Unknown',
    'Answer_sf': 'No Feedback',
}, inplace=True)

# Standardize date formats (convert to datetime)
food_feedback['Date_of_Birth_ff'] = pd.to_datetime(food_feedback['Date_of_Birth_ff'], errors='coerce')
food_feedback['Date_of_Anniversary_ff'] = pd.to_datetime(food_feedback['Date_of_Anniversary_ff'], errors='coerce')
service_feedback['Created_sf'] = pd.to_datetime(service_feedback['Created_sf'], errors='coerce')

# Convert other relevant date fields (if applicable)
# Assuming that other date fields might need similar treatment

# Inspect the data types after conversion
print("\nData Types in Food Feedback:")
print(food_feedback.dtypes)
print("\nData Types in Service Feedback:")
print(service_feedback.dtypes)

# Save the cleaned data (optional)
food_feedback.to_csv('../Cleaned/cleaned_food_feedback.csv', index=False)
service_feedback.to_csv('../Cleaned/cleaned_service_feedback.csv', index=False)

print("\nData preparation completed. Cleaned files saved.")
