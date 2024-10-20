# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
food_feedback = pd.read_csv('../Raw/food_feedback_dump.csv')
service_feedback = pd.read_csv('../Raw/service_feedback_dump.csv')

# Merge feedback data into a single DataFrame for analysis (assuming both datasets have similar structures)
feedback_data = pd.concat([food_feedback, service_feedback], ignore_index=True)

# Assuming the dataset has a 'Rating' column for analysis
# Example ratings are integers ranging from 1 to 10 for the sake of NPS calculation
# For CSAT, let's assume ratings between 1 to 5 (adjust according to your data)

### Step 2: Calculate Net Promoter Score (NPS)

def calculate_nps(ratings):
    promoters = len(ratings[ratings >= 9])  # Ratings 9-10
    passives = len(ratings[(ratings >= 7) & (ratings <= 8)])  # Ratings 7-8
    detractors = len(ratings[ratings <= 6])  # Ratings 0-6
    total_responses = len(ratings)

    nps = ((promoters - detractors) / total_responses) * 100
    return nps

# Apply NPS Calculation (assuming a 'Rating' column exists)
feedback_data['Rating'] = feedback_data['Rating'].fillna(0)  # Fill missing values if any
nps_score = calculate_nps(feedback_data['Rating'])
print(f"Net Promoter Score (NPS): {nps_score}")

### Step 3: Calculate Customer Satisfaction Score (CSAT)

# Define CSAT calculation - assuming ratings 4-5 indicate satisfied customers
def calculate_csat(ratings):
    satisfied_customers = len(ratings[ratings >= 4])  # Ratings 4-5 indicate satisfied
    total_responses = len(ratings)
    csat = (satisfied_customers / total_responses) * 100
    return csat

csat_score = calculate_csat(feedback_data['Rating'])
print(f"Customer Satisfaction Score (CSAT): {csat_score}%")

### Step 4: Calculate Average Rating

average_rating = feedback_data['Rating'].mean()
print(f"Average Rating: {average_rating:.2f}")

### Step 5: Visualize the Results

# Plot NPS, CSAT, and Average Rating for better insight
metrics = ['NPS', 'CSAT', 'Average Rating']
values = [nps_score, csat_score, average_rating]

plt.figure(figsize=(10, 6))
plt.bar(metrics, values, color=['#4CAF50', '#2196F3', '#FF9800'])
plt.title('Customer Feedback Performance Metrics', fontsize=14)
plt.xlabel('Metrics', fontsize=12)
plt.ylabel('Values', fontsize=12)
for index, value in enumerate(values):
    plt.text(index, value + 0.5, f'{value:.2f}', ha='center', fontsize=12)
plt.show()
