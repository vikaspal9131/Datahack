# dataPreparation.py
import pandas as pd
from zenml.steps import step

def load_and_prepare_data() -> pd.DataFrame:
    """Load and merge sales data from raw datasets.

    Returns:
        pd.DataFrame: Merged and prepared sales data.
    """
    sales_data = pd.read_csv('../Raw/sales_dump.csv')
    bill_settlement_data = pd.read_csv('../Raw/bill_settelment_report_dump.csv')
    order_discount_data = pd.read_csv('../Raw/order_discount_summary_dump.csv')

    # Convert 'Invoice_No_' to string type for consistency
    sales_data['Invoice_No_'] = sales_data['Invoice_No_'].astype(str)
    bill_settlement_data['Invoice_No_'] = bill_settlement_data['Invoice_No_'].astype(str)

    # Merge datasets
    merged_data = pd.merge(sales_data, bill_settlement_data, on='Invoice_No_', how='left')

    if 'Order_No_' in order_discount_data.columns:
        order_discount_data['Order_No_'] = order_discount_data['Order_No_'].astype(str)
        merged_data = pd.merge(merged_data, order_discount_data, left_on='Invoice_No_', right_on='Order_No_', how='left')

    # Select and rename relevant columns
    final_data = merged_data[['Date_x', 'Payment_Type_x', 'Order_Type_x', 'Order_Total']]
    final_data.columns = ['Date', 'Payment_Type', 'Order_Type', 'Order_Total']

    return final_data

# Wrap the function with the ZenML step decorator
load_and_prepare_data = step(load_and_prepare_data)
