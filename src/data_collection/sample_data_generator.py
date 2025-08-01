"""
Generate sample data for demonstration purposes
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json
from pathlib import Path

class SampleDataGenerator:
    def __init__(self):
        self.data_dir = Path('../../data')
        self.data_dir.mkdir(exist_ok=True)
        
        # Kenya locations for sample data
        self.kenya_locations = [
            {"name": "Nairobi", "coords": [-1.2921, 36.8219]},
            {"name": "Mombasa", "coords": [-4.0435, 39.6682]},
            {"name": "Kisumu", "coords": [-0.0917, 34.7680]},
            {"name": "Nakuru", "coords": [-0.3031, 36.0800]},
            {"name": "Eldoret", "coords": [0.5143, 35.2698]},
            {"name": "Thika", "coords": [-1.0332, 37.0691]},
            {"name": "Malindi", "coords": [-3.2180, 40.1170]},
            {"name": "Garissa", "coords": [-0.4569, 39.6400]}
        ]
        
        # Sample tweet templates
        self.tweet_templates = [
            "We must #RejectFinanceBill2024! The government cannot burden us with more taxes while corruption thrives. #KenyaProtests",
            "Today we march for our future! #RejectFinanceBill2024 #Maandamano. This bill will destroy small businesses!",
            "The Finance Bill 2024 is unfair to ordinary Kenyans. We demand better governance! #KenyaProtests",
            "Standing with my fellow Kenyans against oppressive taxation. #RejectFinanceBill2024",
            "This bill will increase cost of living for everyone. Time to say NO! #FinanceBill2024 #KenyaProtests",
            "Youth of Kenya unite! We will not accept this financial burden! #RejectFinanceBill2024 #Maandamano",
            "Peaceful protests are our right. We reject this harmful bill! #KenyaProtests",
            "The government must listen to the people! #RejectFinanceBill2024",
            "Small businesses will suffer under this bill. We must resist! #FinanceBill2024",
            "Our voices matter! Join the movement against unfair taxation! #KenyaProtests #RejectFinanceBill2024"
        ]
        
    def generate_sample_tweets(self, num_tweets=1000):
        """Generate sample tweet data"""
        tweets = []
        base_date = datetime.now() - timedelta(days=30)
        
        for i in range(num_tweets):
            # Random date within last 30 days
            random_days = random.randint(0, 30)
            tweet_date = base_date + timedelta(days=random_days)
            
            # Random location
            location = random.choice(self.kenya_locations)
            
            # Random tweet text
            text = random.choice(self.tweet_templates)
            
            # Random engagement metrics
            retweet_count = random.randint(0, 1000)
            favorite_count = random.randint(0, 2000)
            
            # Extract hashtags
            hashtags = []
            if "#RejectFinanceBill2024" in text:
                hashtags.append("RejectFinanceBill2024")
            if "#KenyaProtests" in text:
                hashtags.append("KenyaProtests")
            if "#Maandamano" in text:
                hashtags.append("Maandamano")
            if "#FinanceBill2024" in text:
                hashtags.append("FinanceBill2024")
            
            tweet = {
                'id': f'tweet_{i}',
                'created_at': tweet_date.isoformat(),
                'text': text,
                'user_location': location['name'],
                'coordinates': location['coords'],
                'retweet_count': retweet_count,
                'favorite_count': favorite_count,
                'hashtags': hashtags
            }
            tweets.append(tweet)
        
        # Save to CSV
        df = pd.DataFrame(tweets)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = self.data_dir / f'tweets_{timestamp}.csv'
        df.to_csv(filename, index=False)
        print(f"Generated {len(tweets)} sample tweets saved to {filename}")
        return df
    
    def generate_sample_sentiment(self, tweets_df):
        """Generate sample sentiment data"""
        sentiments = []
        
        for _, tweet in tweets_df.iterrows():
            # Generate realistic sentiment based on content
            if any(word in tweet['text'].lower() for word in ['reject', 'must', 'demand', 'resist']):
                # More negative sentiment for protest language
                polarity = random.uniform(-0.8, -0.2)
                hf_label = 'NEG'
                hf_score = random.uniform(0.7, 0.95)
            elif any(word in tweet['text'].lower() for word in ['unite', 'peaceful', 'voices']):
                # More positive sentiment for unity language
                polarity = random.uniform(0.1, 0.6)
                hf_label = 'POS'
                hf_score = random.uniform(0.6, 0.9)
            else:
                # Neutral
                polarity = random.uniform(-0.3, 0.3)
                hf_label = 'NEU'
                hf_score = random.uniform(0.5, 0.8)
            
            sentiment = {
                'textblob_polarity': polarity,
                'textblob_subjectivity': random.uniform(0.3, 0.9),
                'huggingface_label': hf_label,
                'huggingface_score': hf_score
            }
            sentiments.append(sentiment)
        
        # Create sentiment dataframe with same index
        sentiment_df = pd.DataFrame(sentiments)
        
        # Add tweet data to sentiment df
        combined_df = pd.concat([tweets_df, sentiment_df], axis=1)
        
        # Save to CSV
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        analysis_dir = self.data_dir / 'analysis'
        analysis_dir.mkdir(exist_ok=True)
        filename = analysis_dir / f'sentiment_analysis_{timestamp}.csv'
        combined_df.to_csv(filename, index=False)
        
        # Save stats
        stats = {
            'average_polarity': sentiment_df['textblob_polarity'].mean(),
            'average_subjectivity': sentiment_df['textblob_subjectivity'].mean(),
            'sentiment_distribution': sentiment_df['huggingface_label'].value_counts().to_dict(),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open(analysis_dir / f'sentiment_stats_{timestamp}.json', 'w') as f:
            json.dump(stats, f, indent=4)
        
        print(f"Generated sentiment analysis saved to {filename}")
        return combined_df, stats

def main():
    generator = SampleDataGenerator()
    
    # Generate sample data
    tweets_df = generator.generate_sample_tweets(500)
    sentiment_df, stats = generator.generate_sample_sentiment(tweets_df)
    
    print("\nSample data generation complete!")
    print(f"Average Sentiment: {stats['average_polarity']:.2f}")
    print(f"Sentiment Distribution: {stats['sentiment_distribution']}")

if __name__ == "__main__":
    main()