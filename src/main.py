"""
Main script for the Kenya Protest Tracker
"""

import sys
import time
from pathlib import Path
from datetime import datetime
import logging

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from data_collection.twitter_scraper import TwitterScraper
from analysis.sentiment_analyzer import SentimentAnalyzer
from visualization.map_generator import ProtestMapGenerator
from config.settings import *

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'protest_tracker_{datetime.now().strftime(TIMESTAMP_FORMAT)}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def setup_directories():
    """Create necessary directories if they don't exist"""
    for directory in [DATA_DIR, ANALYSIS_DIR, VISUALIZATION_DIR]:
        Path(directory).mkdir(parents=True, exist_ok=True)

def run_data_collection():
    """Collect tweets about protests"""
    logger.info("Starting data collection...")
    scraper = TwitterScraper()
    
    # Construct search query
    query = " OR ".join(PROTEST_HASHTAGS)
    
    # Get trending hashtags
    trending = scraper.get_trending_hashtags()
    relevant_trending = [tag for tag in trending if any(
        keyword in tag.lower() for keyword in RELEVANT_KEYWORDS
    )]
    if relevant_trending:
        query += " OR " + " OR ".join(relevant_trending)
    
    # Collect tweets
    scraper.collect_tweets(query, max_tweets=TWEET_BATCH_SIZE)
    logger.info("Data collection complete")

def run_sentiment_analysis():
    """Analyze sentiment of collected tweets"""
    logger.info("Starting sentiment analysis...")
    analyzer = SentimentAnalyzer()
    
    # Get latest tweets file
    tweet_files = list(Path(DATA_DIR).glob('tweets_*.csv'))
    if not tweet_files:
        logger.error("No tweet files found!")
        return False
    
    latest_file = max(tweet_files, key=lambda x: x.stat().st_mtime)
    logger.info(f"Analyzing {latest_file}")
    
    # Analyze tweets
    df, stats = analyzer.analyze_dataset(latest_file)
    logger.info("Sentiment analysis complete")
    
    return True

def generate_visualizations():
    """Generate maps and visualizations"""
    logger.info("Generating visualizations...")
    map_generator = ProtestMapGenerator()
    
    # Get latest data files
    tweet_files = list(Path(DATA_DIR).glob('tweets_*.csv'))
    sentiment_files = list(Path(ANALYSIS_DIR).glob('sentiment_analysis_*.csv'))
    
    if not tweet_files or not sentiment_files:
        logger.error("Required data files not found!")
        return False
    
    latest_tweets = max(tweet_files, key=lambda x: x.stat().st_mtime)
    latest_sentiment = max(sentiment_files, key=lambda x: x.stat().st_mtime)
    
    # Generate map
    map_generator.create_protest_map(latest_tweets, latest_sentiment)
    logger.info("Visualization generation complete")
    
    return True

def main():
    """Main execution function"""
    logger.info("Starting Kenya Protest Tracker")
    
    try:
        # Setup
        setup_directories()
        
        # Data collection
        run_data_collection()
        
        # Wait briefly for files to be written
        time.sleep(2)
        
        # Sentiment analysis
        if not run_sentiment_analysis():
            logger.error("Sentiment analysis failed")
            return
        
        # Wait briefly for files to be written
        time.sleep(2)
        
        # Visualization
        if not generate_visualizations():
            logger.error("Visualization generation failed")
            return
        
        logger.info("Kenya Protest Tracker completed successfully")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        return

if __name__ == "__main__":
    main() 