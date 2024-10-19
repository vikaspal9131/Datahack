import os
import shutil

def define_directories(raw_data_path, output_path):
    """
    Define raw data and output directories.
    """
    return raw_data_path, output_path

def create_output_directory(output_path):
    """
    Create the output directory if it doesn't exist.
    """
    os.makedirs(output_path, exist_ok=True)

def define_categories():
    """
    Define the file categories and their corresponding files.
    """
    return {
        'Aggregators': [
            'swiggy_pos_report_dump.csv',
            'swiggy_time_report_dump.csv',
            'zomato_pos_report_dump.csv',
            'zomato_time_report_dump.csv'
        ],
        'Departments': [
            'food_feedback_dump.csv',
            'incentives_dump.csv',
            'internal_transfer_dump.csv',
            'service_feedback_dump.csv'
        ],
        'Inventory': [
            'closing_stock_dump.csv',
            'kot_modification_dump.csv',
            'kot_order_dump.csv',
            'menu.csv',
            'purchase_dump.csv',
            'raw_material_conversion_dump.csv',
            'recipes_dump.csv'
        ],
        'Sales': [
            'bill_settelment_report_dump.csv',
            'cancle_order_summary_dump.csv',
            'order_discount_summary_dump.csv',
            'order_modification_split.csv',
            'order_report_after_print_modification_dump.csv',
            'sales_dump.csv'
        ]
    }

def organize_files(raw_data_dir, output_dir, categories):
    """
    Organize files into category directories.
    """
    print("Organizing files...")
    for category, files in categories.items():
        # Create the category directory inside the output directory
        category_dir = os.path.join(output_dir, category)
        os.makedirs(category_dir, exist_ok=True)
        
        for file in files:
            # Construct the full file path
            file_path = os.path.join(raw_data_dir, file)

            # Debug: Check if the file exists before copying
            if os.path.exists(file_path):
                shutil.copy(file_path, os.path.join(category_dir, file))
                print(f"Copied: {file} to {category_dir}")
            else:
                print(f"File not found: {file_path}")

def main():
    # Define directories
    raw_data_dir, output_dir = define_directories(
        'ML Ops Dataset/PS_DATA/Raw',
        'Organized'
    )
    
    # Create output directory
    create_output_directory(output_dir)
    
    # Define categories
    categories = define_categories()
    
    # Organize files
    organize_files(raw_data_dir, output_dir, categories)
    
    print("All files have been processed.")

if __name__ == "__main__":
    main()