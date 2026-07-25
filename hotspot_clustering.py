import pandas as pd
import sqlite3
from sklearn.cluster import KMeans
import warnings

# Ignore minor scikit-learn warnings for cleaner output
warnings.filterwarnings('ignore')

print("1. Connecting to the Chicago Crime Database...")
conn = sqlite3.connect('chicago_crime_analytics.db')

# Pull only the coordinates we need for the spatial clustering
print("2. Extracting GPS coordinates...")
query = "SELECT incident_id, latitude, longitude FROM crime_incidents"
crime_df = pd.read_sql_query(query, conn)

# Drop any nulls just in case to prevent AI math errors
crime_df = crime_df.dropna(subset=['latitude', 'longitude'])
print(f"Loaded {len(crime_df)} incidents for AI analysis.")

print("3. Running K-Means AI to detect spatial Hotspots...")
# We tell the AI to look for 8 major crime hotspots across the city
kmeans = KMeans(n_clusters=8, random_state=42, n_init=10)

# The AI analyzes the coordinates and assigns a hotspot cluster number (0 to 7) to every crime
crime_df['hotspot_cluster'] = kmeans.fit_predict(crime_df[['latitude', 'longitude']])

print("4. Saving AI Hotspot Insights back to the database...")
# We create a new table just for the AI insights so we don't mess up the raw data
insights_df = crime_df[['incident_id', 'hotspot_cluster']]
insights_df.to_sql('ai_hotspot_insights', conn, if_exists='replace', index=False)

conn.close()
print("Success! The AI has mapped out the hotspots.")
print("Hotspot labels successfully saved to the 'ai_hotspot_insights' table.")