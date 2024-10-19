import pandas as pd

# Load datasets
sales_data = pd.read_csv('../Raw/sales_dump.csv')
bill_settlement_data = pd.read_csv('../Raw/bill_settelment_report_dump.csv')
order_discount_data = pd.read_csv('../Raw/order_discount_summary_dump.csv')

# Print the first few rows of each DataFrame to understand their structure
print("Sales Data:")
print(sales_data.head())
print("\nBill Settlement Data:")
print(bill_settlement_data.head())
print("\nOrder Discount Data:")
print(order_discount_data.head())

# Check the data types of relevant columns
print("\nData Types:")
print("Sales Data Invoice_No_ type:", sales_data['Invoice_No_'].dtype)
print("Bill Settlement Data Invoice_No_ type:", bill_settlement_data['Invoice_No_'].dtype)
print("Order Discount Data Order_No_ type:", order_discount_data['Order_No_'].dtype)

# Convert 'Invoice_No_' columns to string type to avoid type mismatch during merging
sales_data['Invoice_No_'] = sales_data['Invoice_No_'].astype(str)
bill_settlement_data['Invoice_No_'] = bill_settlement_data['Invoice_No_'].astype(str)

# Print to verify conversions
print("\nData Types After Conversion:")
print("Sales Data Invoice_No_ type:", sales_data['Invoice_No_'].dtype)
print("Bill Settlement Data Invoice_No_ type:", bill_settlement_data['Invoice_No_'].dtype)

# Merge sales data with bill settlement data
merged_data = pd.merge(sales_data, bill_settlement_data, on='Invoice_No_', how='left')

# Print columns after merging to check if the merge was successful
print("\nMerged Data Columns After First Merge:")
print(merged_data.columns)

# Now check for 'Order_No_' to merge with order discount data
if 'Order_No_' in order_discount_data.columns:
    # Convert 'Order_No_' in order_discount_data to string to match types
    order_discount_data['Order_No_'] = order_discount_data['Order_No_'].astype(str)
    
    # Merge using Invoice_No_ and Order_No_
    merged_data = pd.merge(merged_data, order_discount_data, left_on='Invoice_No_', right_on='Order_No_', how='left')

# Print columns after merging to check if the merge was successful
print("\nMerged Data Columns After Second Merge:")
print(merged_data.columns)

# Select relevant columns for analysis
relevant_columns = ['Date_x', 'Payment_Type_x', 'Order_Type_x',  'Order_Total']

# Check for missing columns before selecting
missing_columns = [col for col in relevant_columns if col not in merged_data.columns]
if not missing_columns:
    final_data = merged_data[relevant_columns]
    # Rename columns for clarity
    final_data.columns = ['Date', 'Payment_Type', 'Order_Type',  'Order_Total']
    print("\nFinal Data:")
    print(final_data.head())
    
    # Optionally, save the final prepared data to a new CSV file
    final_data.to_csv('../Prepared/final_data.csv', index=False)
    print("\nFinal data saved to 'Prepared/final_data.csv'.")
else:
    print(f"Missing columns: {missing_columns}")
