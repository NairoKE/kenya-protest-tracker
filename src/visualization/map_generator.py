import pandas as pd
import folium
from folium import plugins
import json
from pathlib import Path
from datetime import datetime
import numpy as np
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

class ProtestMapGenerator:
    def __init__(self):
        """Initialize map generator"""
        self.output_dir = Path('../data/visualization')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize geocoder with rate limiting
        self.geolocator = Nominatim(user_agent="kenya_protest_tracker")
        self.geocode = RateLimiter(self.geolocator.geocode, min_delay_seconds=1)
        
        # Kenya's coordinates
        self.kenya_center = [-1.2921, 36.8219]  # Nairobi coordinates
        
    def geocode_location(self, location_str):
        """
        Geocode a location string to coordinates
        
        Args:
            location_str (str): Location string to geocode
        Returns:
            tuple: (latitude, longitude) or None if not found
        """
        try:
            if location_str and isinstance(location_str, str):
                # Add 'Kenya' to improve geocoding accuracy
                if 'kenya' not in location_str.lower():
                    location_str += ', Kenya'
                
                location = self.geocode(location_str)
                if location:
                    return (location.latitude, location.longitude)
        except Exception as e:
            print(f"Error geocoding {location_str}: {str(e)}")
        return None

    def create_protest_map(self, tweets_df, sentiment_df):
        """
        Create an interactive map showing protest locations and sentiment
        
        Args:
            tweets_df (pd.DataFrame): DataFrame containing tweet data
            sentiment_df (pd.DataFrame): DataFrame containing sentiment analysis
        """
        # Merge dataframes
        df = pd.merge(tweets_df, sentiment_df, left_index=True, right_index=True)
        
        # Create base map centered on Kenya
        m = folium.Map(location=self.kenya_center, zoom_start=7)
        
        # Add marker cluster
        marker_cluster = plugins.MarkerCluster().add_to(m)
        
        # Process each tweet
        for idx, row in df.iterrows():
            # Get coordinates
            coords = None
            if row['coordinates']:
                coords = row['coordinates']
            else:
                coords = self.geocode_location(row['user_location'])
            
            if coords:
                # Determine color based on sentiment
                color = 'gray'
                if 'huggingface_label' in row:
                    if row['huggingface_label'] == 'POS':
                        color = 'green'
                    elif row['huggingface_label'] == 'NEG':
                        color = 'red'
                
                # Create popup content
                popup_content = f"""
                <b>Tweet:</b> {row['text']}<br>
                <b>Time:</b> {row['created_at']}<br>
                <b>Sentiment:</b> {row.get('huggingface_label', 'N/A')}<br>
                <b>Confidence:</b> {row.get('huggingface_score', 'N/A'):.2f}
                """
                
                # Add marker
                folium.Marker(
                    location=coords,
                    popup=folium.Popup(popup_content, max_width=300),
                    icon=folium.Icon(color=color)
                ).add_to(marker_cluster)
        
        # Add heatmap layer
        heat_data = []
        for idx, row in df.iterrows():
            coords = None
            if row['coordinates']:
                coords = row['coordinates']
            else:
                coords = self.geocode_location(row['user_location'])
            
            if coords:
                # Weight by engagement (retweets + favorites)
                weight = row['retweet_count'] + row['favorite_count']
                heat_data.append([coords[0], coords[1], weight])
        
        plugins.HeatMap(heat_data).add_to(m)
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        # Save map
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = self.output_dir / f'protest_map_{timestamp}.html'
        m.save(str(output_file))
        print(f"Map saved to {output_file}")

def main():
    map_generator = ProtestMapGenerator()
    
    # Get latest tweet and sentiment files
    data_dir = Path('../data')
    analysis_dir = data_dir / 'analysis'
    
    tweet_files = list(data_dir.glob('tweets_*.csv'))
    sentiment_files = list(analysis_dir.glob('sentiment_analysis_*.csv'))
    
    if not tweet_files or not sentiment_files:
        print("Required data files not found!")
        return
    
    latest_tweets = pd.read_csv(max(tweet_files, key=lambda x: x.stat().st_mtime))
    latest_sentiment = pd.read_csv(max(sentiment_files, key=lambda x: x.stat().st_mtime))
    
    # Generate map
    map_generator.create_protest_map(latest_tweets, latest_sentiment)

if __name__ == "__main__":
    main() 