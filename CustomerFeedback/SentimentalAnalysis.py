# Import necessary libraries
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

# Load the datasets
# Assuming the CSV files are named as per your earlier data description
food_feedback = pd.read_csv('../Raw/food_feedback_dump.csv')
service_feedback = pd.read_csv('../Raw/service_feedback_dump.csv')

# Function to clean text data
def clean_text(text):
    if isinstance(text, str):
        return text.lower().strip()
    return ''

# Function to perform sentiment analysis using TextBlob
def get_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity  # Returns a value between -1 (negative) and 1 (positive)

# Clean the feedback text data
food_feedback['Answer_ff'] = food_feedback['Answer_ff'].apply(clean_text)
service_feedback['Answer_sf'] = service_feedback['Answer_sf'].apply(clean_text)

# Perform sentiment analysis on food feedback
food_feedback['Sentiment_Score'] = food_feedback['Answer_ff'].apply(get_sentiment)

# Classify the sentiment based on the score
food_feedback['Sentiment_Type'] = food_feedback['Sentiment_Score'].apply(
    lambda x: 'Positive' if x > 0 else 'Negative' if x < 0 else 'Neutral'
)

# Perform sentiment analysis on service feedback
service_feedback['Sentiment_Score'] = service_feedback['Answer_sf'].apply(get_sentiment)

# Classify the sentiment based on the score
service_feedback['Sentiment_Type'] = service_feedback['Sentiment_Score'].apply(
    lambda x: 'Positive' if x > 0 else 'Negative' if x < 0 else 'Neutral'
)

# Visualize the sentiment distribution for food feedback
plt.figure(figsize=(8, 6))
food_sentiment_counts = food_feedback['Sentiment_Type'].value_counts()
food_sentiment_counts.plot(kind='bar', color=['green', 'red', 'blue'])
plt.title('Food Feedback Sentiment Distribution')
plt.xlabel('Sentiment Type')
plt.ylabel('Count')
plt.show()

# Visualize the sentiment distribution for service feedback
plt.figure(figsize=(8, 6))
service_sentiment_counts = service_feedback['Sentiment_Type'].value_counts()
service_sentiment_counts.plot(kind='bar', color=['green', 'red', 'blue'])
plt.title('Service Feedback Sentiment Distribution')
plt.xlabel('Sentiment Type')
plt.ylabel('Count')
plt.show()

# Display some statistics on the sentiment analysis
print("Food Feedback Sentiment Analysis:")
print(food_feedback['Sentiment_Type'].value_counts())

print("\nService Feedback Sentiment Analysis:")
print(service_feedback['Sentiment_Type'].value_counts())

# Optional: Save the results to a new CSV file for further analysis
food_feedback.to_csv('food_feedback_sentiment_analysis.csv', index=False)
service_feedback.to_csv('service_feedback_sentiment_analysis.csv', index=False)
