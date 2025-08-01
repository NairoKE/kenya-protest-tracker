import tweepy
import pandas as pd
import json
from datetime import datetime
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

class TwitterScraper:
    def __init__(self):
        """Initialize Twitter API client"""
        self.api_key = os.getenv('TWITTER_API_KEY')
        self.api_secret = os.getenv('TWITTER_API_SECRET')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        
        # Initialize API client
        auth = tweepy.OAuthHandler(self.api_key, self.api_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)
        
        # Create data directory if it doesn't exist
        self.data_dir = Path('../data')
        self.data_dir.mkdir(exist_ok=True)

    def collect_tweets(self, query, max_tweets=10000):
        """
        Collect tweets based on search query
        
        Args:
            query (str): Search query (hashtags, keywords)
            max_tweets (int): Maximum number of tweets to collect
        """
        tweets = []
        try:
            # Search tweets
            for tweet in tweepy.Cursor(self.api.search_tweets,
                                     q=query,
                                     lang="en",
                                     tweet_mode="extended").items(max_tweets):
                
                tweet_data = {
                    'id': tweet.id,
                    'created_at': tweet.created_at,
                    'text': tweet.full_text,
                    'user_location': tweet.user.location,
                    'coordinates': tweet.coordinates,
                    'retweet_count': tweet.retweet_count,
                    'favorite_count': tweet.favorite_count,
                    'hashtags': [hashtag['text'] for hashtag in tweet.entities['hashtags']]
                }
                tweets.append(tweet_data)
                
            # Save to CSV
            df = pd.DataFrame(tweets)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = self.data_dir / f'tweets_{timestamp}.csv'
            df.to_csv(filename, index=False)
            print(f"Collected {len(tweets)} tweets. Saved to {filename}")
            
        except Exception as e:
            print(f"Error collecting tweets: {str(e)}")
            
    def get_trending_hashtags(self, woeid=1528488):  # WOEID for Nairobi, Kenya
        """Get trending hashtags in Kenya"""
        try:
            trends = self.api.get_place_trends(woeid)
            return [trend['name'] for trend in trends[0]['trends'] if trend['name'].startswith('#')]
        except Exception as e:
            print(f"Error getting trends: {str(e)}")
            return []

def main():
    scraper = TwitterScraper()
    
    # Define search query
    hashtags = [
        "#RejectFinanceBill2024",
        "#FinanceBill2024",
        "#KenyaProtests",
        "#Maandamano"  # Swahili word for demonstrations
    ]
    query = " OR ".join(hashtags)
    
    # Get trending hashtags and add relevant ones to search
    trending = scraper.get_trending_hashtags()
    relevant_trending = [tag for tag in trending if any(
        keyword in tag.lower() for keyword in ['protest', 'finance', 'bill', 'kenya']
    )]
    if relevant_trending:
        query += " OR " + " OR ".join(relevant_trending)
    
    # Collect tweets
    scraper.collect_tweets(query)

if __name__ == "__main__":
    main() 