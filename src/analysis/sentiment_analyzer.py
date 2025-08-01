import pandas as pd
import numpy as np
from textblob import TextBlob
from transformers import pipeline
from pathlib import Path
import json
from datetime import datetime

class SentimentAnalyzer:
    def __init__(self):
        """Initialize sentiment analysis tools"""
        # Initialize HuggingFace sentiment analysis pipeline
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="finiteautomata/bertweet-base-sentiment-analysis"
        )
        
        # Create output directory if it doesn't exist
        self.output_dir = Path('../data/analysis')
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def analyze_tweet(self, text):
        """
        Analyze sentiment of a single tweet using both TextBlob and HuggingFace
        
        Args:
            text (str): Tweet text
        Returns:
            dict: Sentiment scores and labels
        """
        # TextBlob analysis
        blob = TextBlob(text)
        textblob_polarity = blob.sentiment.polarity
        textblob_subjectivity = blob.sentiment.subjectivity
        
        # HuggingFace analysis
        huggingface_result = self.sentiment_pipeline(text)[0]
        
        return {
            'textblob_polarity': textblob_polarity,
            'textblob_subjectivity': textblob_subjectivity,
            'huggingface_label': huggingface_result['label'],
            'huggingface_score': huggingface_result['score']
        }

    def analyze_dataset(self, input_file):
        """
        Analyze sentiment for all tweets in a dataset
        
        Args:
            input_file (str): Path to input CSV file
        """
        # Read tweets
        df = pd.read_csv(input_file)
        
        # Initialize lists for results
        sentiments = []
        
        # Analyze each tweet
        for text in df['text']:
            sentiment = self.analyze_tweet(text)
            sentiments.append(sentiment)
        
        # Add sentiment results to dataframe
        sentiment_df = pd.DataFrame(sentiments)
        df = pd.concat([df, sentiment_df], axis=1)
        
        # Calculate aggregate statistics
        stats = {
            'average_polarity': df['textblob_polarity'].mean(),
            'average_subjectivity': df['textblob_subjectivity'].mean(),
            'sentiment_distribution': df['huggingface_label'].value_counts().to_dict(),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        df.to_csv(self.output_dir / f'sentiment_analysis_{timestamp}.csv', index=False)
        
        with open(self.output_dir / f'sentiment_stats_{timestamp}.json', 'w') as f:
            json.dump(stats, f, indent=4)
        
        return df, stats

def main():
    analyzer = SentimentAnalyzer()
    
    # Get latest tweets file
    data_dir = Path('../data')
    tweet_files = list(data_dir.glob('tweets_*.csv'))
    if not tweet_files:
        print("No tweet files found!")
        return
    
    latest_file = max(tweet_files, key=lambda x: x.stat().st_mtime)
    print(f"Analyzing {latest_file}")
    
    # Analyze tweets
    df, stats = analyzer.analyze_dataset(latest_file)
    
    # Print summary
    print("\nAnalysis Complete!")
    print(f"Average Polarity: {stats['average_polarity']:.2f}")
    print(f"Average Subjectivity: {stats['average_subjectivity']:.2f}")
    print("\nSentiment Distribution:")
    for label, count in stats['sentiment_distribution'].items():
        print(f"{label}: {count}")

if __name__ == "__main__":
    main() 