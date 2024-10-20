# main.py
from zenml.pipelines import pipeline
from dataPreparation import load_and_prepare_data
from basicTraining import train_model
from EDA import load_and_prepare_data

def sales_analysis_pipeline() -> None:  # Specify the output type if needed
    """Links all the steps together in a pipeline."""
    data = load_and_prepare_data()  # Step for loading and preparing data
    predictions = train_model(data=data)  # Step for training the model
    load_and_prepare_data(data=data)  # Pass the loaded data to the EDA step

# Instantiate the pipeline
sales_pipeline = pipeline(sales_analysis_pipeline)

# Run the pipeline
if __name__ == "__main__":
    sales_pipeline()  # Call the pipeline directly
