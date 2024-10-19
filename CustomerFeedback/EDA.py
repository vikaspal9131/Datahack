import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set up visualization style
sns.set(style='whitegrid')

# Load the cleaned datasets
food_feedback = pd.read_csv('../Cleaned/cleaned_food_feedback.csv')
service_feedback = pd.read_csv('../Cleaned/cleaned_service_feedback.csv')

# Inspect the first few rows of each dataset
print("Food Feedback Data:")
print(food_feedback.head())
print("\nService Feedback Data:")
print(service_feedback.head())

# Summary statistics for food feedback
print("\nFood Feedback Summary Statistics:")
print(food_feedback.describe(include='all'))

# Summary statistics for service feedback
print("\nService Feedback Summary Statistics:")
print(service_feedback.describe(include='all'))

# Visualizing distribution of feedback answers
plt.figure(figsize=(10, 5))
sns.countplot(data=food_feedback, x='Answer_ff', palette='Set2')
plt.title('Distribution of Feedback Answers (Food Feedback)')
plt.xlabel('Feedback Answer')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(10, 5))
sns.countplot(data=service_feedback, x='Answer_sf', palette='Set2')
plt.title('Distribution of Feedback Answers (Service Feedback)')
plt.xlabel('Feedback Answer')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()

# Analyzing the relationship between feedback and order type in food feedback
plt.figure(figsize=(10, 5))
sns.countplot(data=food_feedback, x='Order_Type_ff', hue='Answer_ff', palette='Set1')
plt.title('Feedback by Order Type (Food Feedback)')
plt.xlabel('Order Type')
plt.ylabel('Count')
plt.legend(title='Feedback Answer')
plt.xticks(rotation=45)
plt.show()

# Analyzing the relationship between feedback and order type in service feedback
plt.figure(figsize=(10, 5))
sns.countplot(data=service_feedback, x='Order_Type_sf', hue='Answer_sf', palette='Set1')
plt.title('Feedback by Order Type (Service Feedback)')
plt.xlabel('Order Type')
plt.ylabel('Count')
plt.legend(title='Feedback Answer')
plt.xticks(rotation=45)
plt.show()

# Analyzing trends over time in food feedback
food_feedback['Created_ff'] = pd.to_datetime(food_feedback['Created_ff'])
food_feedback.set_index('Created_ff', inplace=True)
food_feedback.resample('M').count()['Answer_ff'].plot(figsize=(12, 6), marker='o')
plt.title('Monthly Trend of Food Feedback')
plt.xlabel('Date')
plt.ylabel('Count of Feedback')
plt.grid()
plt.show()

# Analyzing trends over time in service feedback
service_feedback['Created_sf'] = pd.to_datetime(service_feedback['Created_sf'])
service_feedback.set_index('Created_sf', inplace=True)
service_feedback.resample('M').count()['Answer_sf'].plot(figsize=(12, 6), marker='o', color='orange')
plt.title('Monthly Trend of Service Feedback')
plt.xlabel('Date')
plt.ylabel('Count of Feedback')
plt.grid()
plt.show()

# Correlation heatmap (if numeric fields are available in the datasets)
# Correlation heatmap (only for numeric fields in the datasets)
# For Food Feedback
plt.figure(figsize=(10, 8))
numeric_cols_food = food_feedback.select_dtypes(include=['float64', 'int64'])  # Select only numeric columns
correlation_matrix = numeric_cols_food.corr()  # Compute correlation matrix
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap (Food Feedback)')
plt.show()

# For Service Feedback
plt.figure(figsize=(10, 8))
numeric_cols_service = service_feedback.select_dtypes(include=['float64', 'int64'])  # Select only numeric columns
correlation_matrix_service = numeric_cols_service.corr()  # Compute correlation matrix
sns.heatmap(correlation_matrix_service, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap (Service Feedback)')
plt.show()