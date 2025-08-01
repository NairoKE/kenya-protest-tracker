# Kenya Protest Tracker & Sentiment Analyzer

## Overview
This project analyzes protests in Kenya related to the Finance Bill 2024 using Twitter/X data. It provides insights through:
- Protest location mapping
- Sentiment analysis
- Time-series trend analysis
- Topic modeling of key concerns
- Policy impact risk assessment using LLMs

## Features
- Real-time Twitter data collection using #RejectFinanceBill2024 and related hashtags
- Interactive map visualization of protest locations
- Sentiment analysis of protest-related tweets
- Daily topic extraction and trend analysis
- AI-powered policy impact risk scoring

## Setup
1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file with your Twitter API credentials:
```
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
```

## Project Structure
- `src/`
  - `data_collection/`: Twitter API integration and data gathering
  - `analysis/`: Sentiment analysis and topic modeling
  - `visualization/`: Map generation and data visualization
  - `models/`: LLM integration for risk scoring
- `data/`: Storage for collected and processed data
- `notebooks/`: Jupyter notebooks for analysis and visualization
- `config/`: Configuration files

## Usage
1. Run data collection:
```bash
python src/data_collection/twitter_scraper.py
```
2. Generate analysis:
```bash
python src/analysis/analyze_protests.py
```
3. View visualizations:
```bash
python src/visualization/generate_maps.py
```

## License
MIT License 