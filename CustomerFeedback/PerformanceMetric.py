# Import necessary libraries
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

# Load the datasets
food_feedback = pd.read_csv('../Raw/food_feedback_dump.csv')
service_feedback = pd.read_csv('../Raw/service_feedback_dump.csv')

# Merge feedback data into a single DataFrame for analysis
feedback_data = pd.concat([food_feedback, service_feedback], ignore_index=True)

# Display first few rows to understand the data structure
print(feedback_data.head())

### Step 1: Customer Satisfaction Score (CSAT)

# We will use the feedback answer fields (assuming they contain textual responses from customers)
# Filter responses that indicate customer satisfaction based on positive keywords

def calculate_csat(feedback_column):
    positive_responses = feedback_column.str.contains('good|excellent|great|satisfied|happy', case=False, na=False).sum()
    total_responses = len(feedback_column)
    csat = (positive_responses / total_responses) * 100
    return csat

# Calculate CSAT for food and service feedback separately
csat_score_food = calculate_csat(feedback_data['Answer_ff'])
csat_score_service = calculate_csat(feedback_data['Answer_sf'])

print(f"Customer Satisfaction Score (CSAT) for Food: {csat_score_food}%")
print(f"Customer Satisfaction Score (CSAT) for Service: {csat_score_service}%")

### Step 2: Sentiment Analysis on Customer Feedback

# Perform sentiment analysis using TextBlob to understand overall customer sentiment
def analyze_sentiment(text):
    analysis = TextBlob(str(text))
    return analysis.sentiment.polarity  # Polarity ranges from -1 (negative) to 1 (positive)

# Apply sentiment analysis on both food and service feedback columns
feedback_data['Sentiment_Score_Food'] = feedback_data['Answer_ff'].apply(analyze_sentiment)
feedback_data['Sentiment_Score_Service'] = feedback_data['Answer_sf'].apply(analyze_sentiment)

# Classify the sentiment as positive, negative, or neutral for both food and service feedback
feedback_data['Sentiment_Label_Food'] = feedback_data['Sentiment_Score_Food'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))
feedback_data['Sentiment_Label_Service'] = feedback_data['Sentiment_Score_Service'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))

# Display sentiment distribution
sentiment_counts_food = feedback_data['Sentiment_Label_Food'].value_counts()
sentiment_counts_service = feedback_data['Sentiment_Label_Service'].value_counts()

print("\nSentiment Distribution for Food Feedback:")
print(sentiment_counts_food)

print("\nSentiment Distribution for Service Feedback:")
print(sentiment_counts_service)

### Step 3: Visualization of Sentiment Analysis

# Plot the distribution of sentiment labels for food feedback
plt.figure(figsize=(8, 5))
sentiment_counts_food.plot(kind='bar', color=['#4CAF50', '#F44336', '#FFC107'])
plt.title('Customer Feedback Sentiment Analysis for Food', fontsize=14)
plt.xlabel('Sentiment', fontsize=12)
plt.ylabel('Number of Responses', fontsize=12)
plt.xticks(rotation=0)
plt.show()

# Plot the distribution of sentiment labels for service feedback
plt.figure(figsize=(8, 5))
sentiment_counts_service.plot(kind='bar', color=['#4CAF50', '#F44336', '#FFC107'])
plt.title('Customer Feedback Sentiment Analysis for Service', fontsize=14)
plt.xlabel('Sentiment', fontsize=12)
plt.ylabel('Number of Responses', fontsize=12)
plt.xticks(rotation=0)
plt.show()

### Step 4: Visualize CSAT Score

# Plot the CSAT Scores for food and service feedback
plt.figure(figsize=(6, 4))
plt.bar(['Food CSAT Score', 'Service CSAT Score'], [csat_score_food, csat_score_service], color=['#2196F3', '#FF9800'])
plt.title('Customer Satisfaction Score (CSAT)', fontsize=14)
plt.ylim(0, 100)
for i, score in enumerate([csat_score_food, csat_score_service]):
    plt.text(i, score + 2, f'{score:.2f}%', ha='center', fontsize=12)
plt.show()