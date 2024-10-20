# Importing necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
import nltk
from wordcloud import WordCloud

# Downloading NLTK data for text processing
nltk.download('punkt')

# Load the datasets
food_feedback = pd.read_csv('../Raw/food_feedback_dump.csv')
service_feedback = pd.read_csv('../Raw/service_feedback_dump.csv')

# Step 1: Data Preprocessing
# Fill missing values with placeholder text (if any)
food_feedback.fillna('No Response', inplace=True)
service_feedback.fillna('No Response', inplace=True)

# Step 2: Sentiment Analysis Function
def get_sentiment(text):
    analysis = TextBlob(str(text))
    return analysis.sentiment.polarity

# Step 3: Applying Sentiment Analysis to Feedback Data
food_feedback['Sentiment_Score'] = food_feedback['Answer_ff'].apply(get_sentiment)
service_feedback['Sentiment_Score'] = service_feedback['Answer_sf'].apply(get_sentiment)

# Step 4: Classify Sentiments into Categories
def classify_sentiment(score):
    if score > 0:
        return 'Positive'
    elif score < 0:
        return 'Negative'
    else:
        return 'Neutral'

food_feedback['Sentiment_Type'] = food_feedback['Sentiment_Score'].apply(classify_sentiment)
service_feedback['Sentiment_Type'] = service_feedback['Sentiment_Score'].apply(classify_sentiment)

# Step 5: Visualizing Sentiment Distribution
plt.figure(figsize=(10, 5))
sns.countplot(x='Sentiment_Type', data=food_feedback, palette='coolwarm')
plt.title('Food Feedback Sentiment Distribution', fontsize=14)
plt.xlabel('Sentiment Type', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.show()

plt.figure(figsize=(10, 5))
sns.countplot(x='Sentiment_Type', data=service_feedback, palette='coolwarm')
plt.title('Service Feedback Sentiment Distribution', fontsize=14)
plt.xlabel('Sentiment Type', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.show()

# Step 6: Generating Word Clouds for Frequent Feedback Terms
food_text = ' '.join(food_feedback['Answer_ff'].astype(str))
service_text = ' '.join(service_feedback['Answer_sf'].astype(str))

food_wordcloud = WordCloud(background_color='white', max_words=100, width=800, height=400).generate(food_text)
service_wordcloud = WordCloud(background_color='white', max_words=100, width=800, height=400).generate(service_text)

# Display the Word Clouds
plt.figure(figsize=(10, 5))
plt.imshow(food_wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Most Common Words in Food Feedback', fontsize=14)
plt.show()

plt.figure(figsize=(10, 5))
plt.imshow(service_wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Most Common Words in Service Feedback', fontsize=14)
plt.show()

# Step 7: Key Insights from Feedback
# Grouping feedback to understand the overall sentiment
food_sentiment_summary = food_feedback['Sentiment_Type'].value_counts(normalize=True) * 100
service_sentiment_summary = service_feedback['Sentiment_Type'].value_counts(normalize=True) * 100

print("Food Feedback Sentiment Breakdown (%):")
print(food_sentiment_summary)
print("\nService Feedback Sentiment Breakdown (%):")
print(service_sentiment_summary)

# Step 8: Identifying Top Positive and Negative Comments
# Top 5 Positive Feedback Comments for Food
print("\nTop 5 Positive Food Feedback Comments:")
print(food_feedback[food_feedback['Sentiment_Type'] == 'Positive']['Answer_ff'].head(5))

# Top 5 Negative Feedback Comments for Food
print("\nTop 5 Negative Food Feedback Comments:")
print(food_feedback[food_feedback['Sentiment_Type'] == 'Negative']['Answer_ff'].head(5))

# Top 5 Positive Feedback Comments for Service
print("\nTop 5 Positive Service Feedback Comments:")
print(service_feedback[service_feedback['Sentiment_Type'] == 'Positive']['Answer_sf'].head(5))

# Top 5 Negative Feedback Comments for Service
print("\nTop 5 Negative Service Feedback Comments:")
print(service_feedback[service_feedback['Sentiment_Type'] == 'Negative']['Answer_sf'].head(5))
