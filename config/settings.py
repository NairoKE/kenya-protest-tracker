"""
Configuration settings for the Kenya Protest Tracker
"""

# Twitter API Settings
TWEET_BATCH_SIZE = 10000
TWEET_LANGUAGE = "en"

# Hashtags and Keywords
PROTEST_HASHTAGS = [
    "#RejectFinanceBill2024",
    "#FinanceBill2024",
    "#KenyaProtests",
    "#Maandamano"
]

RELEVANT_KEYWORDS = [
    "protest",
    "finance",
    "bill",
    "kenya",
    "demonstration",
    "march",
    "strike"
]

# Geographical Settings
KENYA_CENTER = [-1.2921, 36.8219]  # Nairobi coordinates
KENYA_WOEID = 1528488  # Where On Earth ID for Kenya (used in Twitter API)

# Map Settings
MAP_ZOOM_START = 7
MARKER_COLORS = {
    'POS': 'green',
    'NEG': 'red',
    'NEU': 'gray'
}

# File Paths
DATA_DIR = "data"
ANALYSIS_DIR = "data/analysis"
VISUALIZATION_DIR = "data/visualization"

# Analysis Settings
SENTIMENT_MODEL = "finiteautomata/bertweet-base-sentiment-analysis"
MIN_CONFIDENCE_THRESHOLD = 0.7  # Minimum confidence score for sentiment classification

# Time Settings
TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"
DATE_FORMAT = "%Y-%m-%d"

# Geocoding Settings
GEOCODING_DELAY = 1  # Delay between geocoding requests in seconds 