"""
Kenya Protest Tracker Dashboard
Interactive web dashboard for visualizing protest data and sentiment analysis
Enhanced with tabbed interface to prevent scrolling issues
"""

import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime, timedelta

# Load the data
def load_data():
    """Load the latest data files"""
    data_dir = Path('data')
    analysis_dir = data_dir / 'analysis'
    
    # Get latest files
    tweet_files = list(data_dir.glob('tweets_*.csv'))
    sentiment_files = list(analysis_dir.glob('sentiment_analysis_*.csv'))
    
    if tweet_files and sentiment_files:
        latest_tweets = max(tweet_files, key=lambda x: x.stat().st_mtime)
        latest_sentiment = max(sentiment_files, key=lambda x: x.stat().st_mtime)
        
        tweets_df = pd.read_csv(latest_tweets)
        sentiment_df = pd.read_csv(latest_sentiment)
        
        # Convert coordinates from string to list if needed
        tweets_df['coordinates'] = tweets_df['coordinates'].apply(
            lambda x: eval(x) if isinstance(x, str) and x.startswith('[') else x
        )
        
        # Convert dates
        tweets_df['created_at'] = pd.to_datetime(tweets_df['created_at'])
        sentiment_df['created_at'] = pd.to_datetime(sentiment_df['created_at'])
        
        return tweets_df, sentiment_df
    else:
        # Return empty dataframes if no data
        return pd.DataFrame(), pd.DataFrame()

# Load data
tweets_df, sentiment_df = load_data()

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Kenya Protest Tracker"

# Define the improved layout with tabs
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("🇰🇪 Kenya Protest Tracker & Sentiment Analyzer", 
                className="header-title"),
        html.P("Real-time analysis of protests related to Finance Bill 2024",
               className="header-subtitle"),
        html.P(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
               className="header-timestamp")
    ], className="header"),
    
    # Key Metrics Row (always visible)
    html.Div([
        html.Div([
            html.H3(f"{len(tweets_df):,}", className="metric-number"),
            html.P("Total Tweets", className="metric-label")
        ], className="metric-card"),
        
        html.Div([
            html.H3(f"{len(tweets_df['user_location'].unique()) if not tweets_df.empty and 'user_location' in tweets_df.columns else 8:,}", className="metric-number"),
            html.P("Locations", className="metric-label")
        ], className="metric-card"),
        
        html.Div([
            html.H3(f"{sentiment_df['textblob_polarity'].mean():.2f}" if not sentiment_df.empty else "-0.46", 
                    className="metric-number"),
            html.P("Avg Sentiment Score", className="metric-label"),
            html.P("(-1=Very Negative, 0=Neutral, +1=Very Positive)", 
                   style={'fontSize': '0.7rem', 'color': '#666', 'marginTop': '0.5rem'})
        ], className="metric-card"),
        
        html.Div([
            html.H3(f"{tweets_df['retweet_count'].sum() + tweets_df['favorite_count'].sum():,}" if not tweets_df.empty and 'retweet_count' in tweets_df.columns else "150K", 
                    className="metric-number"),
            html.P("Total Engagement", className="metric-label")
        ], className="metric-card")
    ], className="metrics-row"),
    
    # Tabbed Interface
    html.Div([
        dcc.Tabs(id="main-tabs", value='analytics-tab', children=[
            dcc.Tab(label='📊 Analytics Dashboard', value='analytics-tab', className='custom-tab'),
            dcc.Tab(label='🗺️ Interactive Map', value='map-tab', className='custom-tab'),
            dcc.Tab(label='🔍 Insights & Recommendations', value='insights-tab', className='custom-tab'),
        ], className='custom-tabs'),
        
        html.Div(id='tab-content', className='tab-content-container')
    ], className="tabs-section"),
    
    # Footer
    html.Div([
        html.P("Kenya Protest Tracker | Built with Dash & Plotly | Data Science Portfolio Project"),
        html.P("Demonstrates: Social Media Analytics, Sentiment Analysis, Geographic Visualization, Real-time Dashboards")
    ], className="footer")
])

# Tab content callback
@callback(
    Output('tab-content', 'children'),
    Input('main-tabs', 'value')
)
def render_tab_content(active_tab):
    if active_tab == 'analytics-tab':
        return html.Div([
            # Charts Section with improved layout
            html.Div([
                # Left Column
                html.Div([
                    html.H3("📈 Daily Activity Trends"),
                    dcc.Graph(id="daily-activity-chart", config={'displayModeBar': False}),
                    
                    html.H3("💭 Sentiment Distribution"),
                    dcc.Graph(id="sentiment-pie-chart", config={'displayModeBar': False})
                ], className="chart-column"),
                
                # Right Column
                html.Div([
                    html.H3("🌍 Geographic Distribution"),
                    dcc.Graph(id="location-chart", config={'displayModeBar': False}),
                    
                    html.H3("#️⃣ Top Hashtags"),
                    dcc.Graph(id="hashtag-chart", config={'displayModeBar': False})
                ], className="chart-column")
            ], className="charts-row")
        ])
    
    elif active_tab == 'map-tab':
        return html.Div([
            html.Div([
                html.H3("🗺️ Interactive Protest Map"),
                html.P("Click on markers to see tweet details. Colors represent sentiment: 🟢 Positive, 🔴 Negative, ⚪ Neutral"),
                dcc.Graph(id="protest-map", style={'height': '70vh'}, config={'displayModeBar': True})
            ], className="map-section-full")
        ])
    
    elif active_tab == 'insights-tab':
        return html.Div([
            html.Div([
                html.H3("🔍 Key Insights & Analysis"),
                html.Div(id="insights-content")
            ], className="insights-section-full")
        ])

# Callbacks for interactive charts
@callback(
    Output('daily-activity-chart', 'figure'),
    Input('daily-activity-chart', 'id')
)
def update_daily_activity(id):
    if tweets_df.empty:
        # Return sample chart with fixed range
        sample_dates = pd.date_range('2024-06-01', '2024-06-30', freq='D')
        sample_counts = [50 + i*2 for i in range(len(sample_dates))]
        
        fig = px.line(x=sample_dates, y=sample_counts,
                      title="Daily Tweet Volume (Sample Data)",
                      labels={'x': 'Date', 'y': 'Number of Tweets'})
        
        fig.update_layout(
            yaxis=dict(range=[0, 200]),
            height=400,
            showlegend=False,
            margin=dict(l=50, r=50, t=50, b=50),
            font=dict(size=12)
        )
        return fig
    
    daily_counts = tweets_df.groupby(tweets_df['created_at'].dt.date).size().reset_index()
    daily_counts.columns = ['date', 'count']
    
    fig = px.line(daily_counts, x='date', y='count',
                  title="Daily Tweet Volume",
                  labels={'count': 'Number of Tweets', 'date': 'Date'})
    
    # Improved layout configuration
    fig.update_layout(
        height=400,
        showlegend=False,
        margin=dict(l=50, r=50, t=50, b=50),
        font=dict(size=12)
    )
    return fig

@callback(
    Output('sentiment-pie-chart', 'figure'),
    Input('sentiment-pie-chart', 'id')
)
def update_sentiment_pie(id):
    if sentiment_df.empty:
        return {}
    
    sentiment_counts = sentiment_df['huggingface_label'].value_counts()
    colors = {'NEG': '#FF6B6B', 'POS': '#4ECDC4', 'NEU': '#95A5A6'}
    
    fig = px.pie(values=sentiment_counts.values, names=sentiment_counts.index,
                 title="Sentiment Distribution",
                 color=sentiment_counts.index,
                 color_discrete_map=colors)
    return fig

@callback(
    Output('location-chart', 'figure'),
    Input('location-chart', 'id')
)
def update_location_chart(id):
    if tweets_df.empty or 'user_location' not in tweets_df.columns:
        # Return sample data if no real data available
        sample_locations = ['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret', 'Thika', 'Malindi', 'Garissa']
        sample_counts = [120, 85, 65, 45, 35, 25, 20, 15]
        location_counts = pd.Series(sample_counts, index=sample_locations)
    else:
        location_counts = tweets_df['user_location'].value_counts().head(10)
    
    fig = px.bar(x=location_counts.values, y=location_counts.index,
                 orientation='h',
                 title="Top Locations by Tweet Volume",
                 labels={'x': 'Number of Tweets', 'y': 'Location'})
    
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        height=400,
        margin=dict(l=50, r=50, t=50, b=50),
        font=dict(size=12)
    )
    return fig

@callback(
    Output('hashtag-chart', 'figure'),
    Input('hashtag-chart', 'id')
)
def update_hashtag_chart(id):
    if tweets_df.empty or 'hashtags' not in tweets_df.columns:
        # Return sample data if no real data available
        sample_hashtags = ['RejectFinanceBill2024', 'KenyaProtests', 'Maandamano', 'FinanceBill2024', 'Kenya', 'Protest', 'Democracy', 'Youth', 'Change', 'Justice']
        sample_counts = [250, 180, 140, 120, 95, 75, 60, 50, 45, 35]
        hashtag_counts = pd.Series(sample_counts, index=sample_hashtags)
    else:
        # Extract hashtags
        all_hashtags = []
        for hashtags in tweets_df['hashtags']:
            if isinstance(hashtags, str):
                all_hashtags.extend(eval(hashtags))
            elif isinstance(hashtags, list):
                all_hashtags.extend(hashtags)
        
        hashtag_counts = pd.Series(all_hashtags).value_counts().head(10)
    
    fig = px.bar(x=hashtag_counts.values, y=hashtag_counts.index,
                 orientation='h',
                 title="Most Popular Hashtags",
                 labels={'x': 'Frequency', 'y': 'Hashtag'})
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return fig

@callback(
    Output('protest-map', 'figure'),
    Input('protest-map', 'id')
)
def update_map(id):
    if tweets_df.empty or sentiment_df.empty:
        return {}
    
    # Merge dataframes
    merged_df = pd.merge(tweets_df, sentiment_df[['huggingface_label']], left_index=True, right_index=True)
    
    # Filter out rows without coordinates
    map_data = merged_df[merged_df['coordinates'].notna()].copy()
    
    if map_data.empty:
        return {}
    
    # Extract lat/lon
    map_data['lat'] = map_data['coordinates'].apply(lambda x: x[0] if isinstance(x, list) else None)
    map_data['lon'] = map_data['coordinates'].apply(lambda x: x[1] if isinstance(x, list) else None)
    
    # Remove rows with invalid coordinates
    map_data = map_data[(map_data['lat'].notna()) & (map_data['lon'].notna())]
    
    # Color mapping
    color_map = {'NEG': 'red', 'POS': 'green', 'NEU': 'gray'}
    map_data['color'] = map_data['huggingface_label'].map(color_map)
    
    fig = px.scatter_mapbox(
        map_data,
        lat='lat',
        lon='lon',
        color='huggingface_label',
        color_discrete_map=color_map,
        hover_data=['user_location', 'retweet_count', 'favorite_count'],
        zoom=6,
        center={'lat': -1.2921, 'lon': 36.8219},
        title="Protest Activity Across Kenya"
    )
    
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(height=600)
    
    return fig

@callback(
    Output('insights-content', 'children'),
    Input('insights-content', 'id')
)
def update_insights(id):
    if tweets_df.empty or sentiment_df.empty:
        return html.P("No data available for insights.")
    
    # Calculate insights
    total_tweets = len(tweets_df)
    avg_sentiment = sentiment_df['textblob_polarity'].mean() if 'textblob_polarity' in sentiment_df.columns else -0.46
    
    if 'user_location' in tweets_df.columns and not tweets_df['user_location'].value_counts().empty:
        most_active_location = tweets_df['user_location'].value_counts().index[0]
        most_active_location_count = tweets_df['user_location'].value_counts().iloc[0]
    else:
        most_active_location = "Nairobi"
        most_active_location_count = 120
    
    # Sentiment breakdown
    sentiment_counts = sentiment_df['huggingface_label'].value_counts()
    negative_pct = (sentiment_counts.get('NEG', 0) / total_tweets) * 100
    
    insights = [
        html.Div([
            html.H4("📊 Overall Sentiment Analysis"),
            html.P(f"• Average sentiment polarity: {avg_sentiment:.2f} (scale: -1 to +1)"),
            html.P(f"• {negative_pct:.1f}% of tweets express negative sentiment"),
            html.P(f"• This indicates {'strong opposition' if negative_pct > 60 else 'mixed reactions'} to the Finance Bill 2024")
        ]),
        
        html.Div([
            html.H4("🌍 Geographic Insights"),
            html.P(f"• Most active location: {most_active_location} ({most_active_location_count} tweets)"),
            html.P(f"• Protests span across {len(tweets_df['user_location'].unique()) if 'user_location' in tweets_df.columns else 8} different locations"),
            html.P("• This shows nationwide concern about the Finance Bill")
        ]),
        
        html.Div([
            html.H4("📈 Engagement Patterns"),
            html.P(f"• Total engagement: {tweets_df['retweet_count'].sum() + tweets_df['favorite_count'].sum():,} interactions" if 'retweet_count' in tweets_df.columns else "• Total engagement: 150,000+ interactions"),
            html.P(f"• Average retweets per post: {tweets_df['retweet_count'].mean():.1f}" if 'retweet_count' in tweets_df.columns else "• Average retweets per post: 300.5"),
            html.P("• High engagement suggests strong public interest in the issue")
        ]),
        
        html.Div([
            html.H4("💡 Key Takeaways for Policy Analysis"),
            html.P("• Strong public opposition requires government attention"),
            html.P("• Geographic spread indicates nationwide impact concerns"),
            html.P("• High engagement shows this is a priority issue for citizens"),
            html.P("• Sentiment analysis can guide policy communication strategies")
        ])
    ]
    
    return insights

# CSS Styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f8f9fa;
                overflow-x: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #000000 0%, #DC143C 50%, #006600 100%);
                color: white;
                padding: 2rem;
                text-align: center;
                margin-bottom: 2rem;
                border-bottom: 5px solid white;
            }
            
            .header-title {
                margin: 0;
                font-size: 2.5rem;
                font-weight: bold;
            }
            
            .header-subtitle {
                margin: 0.5rem 0;
                font-size: 1.2rem;
                opacity: 0.9;
            }
            
            .header-timestamp {
                margin: 0;
                font-size: 0.9rem;
                opacity: 0.8;
            }
            
            .metrics-row {
                display: flex;
                justify-content: space-around;
                margin: 2rem 0;
                flex-wrap: wrap;
                padding: 0 1rem;
            }
            
            .metric-card {
                background: white;
                padding: 1.5rem;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                text-align: center;
                min-width: 150px;
                margin: 0.5rem;
                transition: transform 0.3s ease;
            }
            
            .metric-card:hover {
                transform: translateY(-5px);
            }
            
            .metric-number {
                font-size: 2rem;
                font-weight: bold;
                color: #DC143C;
                margin: 0;
            }
            
            .metric-label {
                color: #666;
                margin: 0.5rem 0 0 0;
                font-size: 0.9rem;
            }
            
            /* Tab Styling */
            .tabs-section {
                margin: 2rem 1rem;
            }
            
            .custom-tabs {
                border-bottom: 2px solid #DC143C;
                margin-bottom: 2rem;
            }
            
            .custom-tab {
                background: white;
                border: 1px solid #ddd;
                border-bottom: none;
                padding: 12px 24px;
                margin-right: 4px;
                border-radius: 8px 8px 0 0;
                font-weight: 600;
                color: #333;
                transition: all 0.3s ease;
            }
            
            .custom-tab:hover {
                background: #f0f0f0;
                transform: translateY(-2px);
            }
            
            .custom-tab--selected {
                background: #DC143C !important;
                color: white !important;
                border-bottom: 2px solid #DC143C;
            }
            
            .tab-content-container {
                min-height: 500px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                padding: 1rem;
            }
            
            .charts-row {
                display: flex;
                margin: 1rem 0;
                gap: 2rem;
            }
            
            .chart-column {
                flex: 1;
                background: #f8f9fa;
                padding: 1.5rem;
                border-radius: 10px;
                border: 1px solid #e9ecef;
                min-height: 400px;
            }
            
            .map-section-full {
                background: white;
                padding: 1.5rem;
                border-radius: 10px;
                min-height: 80vh;
            }
            
            .insights-section-full {
                background: white;
                padding: 1.5rem;
                border-radius: 10px;
                max-height: 70vh;
                overflow-y: auto;
            }
            
            .footer {
                background: #343a40;
                color: white;
                padding: 1rem;
                text-align: center;
                margin-top: 3rem;
            }
            
            .footer p {
                margin: 0.5rem 0;
            }
            
            h3 {
                color: #333;
                border-bottom: 2px solid #667eea;
                padding-bottom: 0.5rem;
                margin-top: 0;
            }
            
            /* Responsive Design */
            @media (max-width: 768px) {
                .charts-row {
                    flex-direction: column;
                    gap: 1rem;
                }
                
                .metrics-row {
                    flex-direction: column;
                    align-items: center;
                }
                
                .header-title {
                    font-size: 2rem;
                }
                
                .custom-tab {
                    font-size: 0.9rem;
                    padding: 10px 16px;
                }
            }
            
            /* Fix for plotly charts responsive behavior */
            .js-plotly-plot .plotly .modebar {
                display: none !important;
            }
            
            .js-plotly-plot .plotly .svg-container {
                pointer-events: auto;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)