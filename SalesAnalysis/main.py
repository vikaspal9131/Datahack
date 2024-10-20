# main.py
from zenml.pipelines import pipeline
from dataPreparation import load_and_prepare_data
from basicTraining import train_model
from EDA import perform_eda

@pipeline
def sales_analysis_pipeline(importer, trainer, eda):
    """Links all the steps together in a pipeline."""
    data = importer()  # Step for loading and preparing data
    predictions = trainer(data=data)  # Step for training the model
    eda(data=data)  # Pass the loaded data to the EDA step

# Create the pipeline with instantiated steps
sales_pipeline = sales_analysis_pipeline(
    importer=load_and_prepare_data(),  # Instantiate the step
    trainer=train_model(),  # Instantiate the step
    eda=perform_eda()  # Instantiate the step
)

# Run the pipeline
if __name__ == "__main__":
    sales_pipeline()
