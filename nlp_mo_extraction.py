import pandas as pd
import sqlite3
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings

warnings.filterwarnings('ignore')

print("1. Connecting to the Chicago Crime Database...")
conn = sqlite3.connect('chicago_crime_analytics.db')

print("2. Fetching Crime Narratives...")
query = "SELECT incident_id, fir_narrative FROM crime_incidents"
df = pd.read_sql_query(query, conn)

# Fill any blank text with a placeholder so the AI doesn't crash
df['fir_narrative'] = df['fir_narrative'].fillna('Unknown incident')
print(f"Loaded {len(df)} narratives for NLP extraction.")

print("3. Running NLP (TF-IDF) to extract Modus Operandi (MO)...")
# The Vectorizer will read the text and ignore common filler words ('stop_words')
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
tfidf_matrix = vectorizer.fit_transform(df['fir_narrative'])

# Get the list of vocabulary words the AI found
feature_names = np.array(vectorizer.get_feature_names_out())

# A quick function to grab the top 2 most important words from each paragraph
def get_top_keywords(row_idx):
    # Get the math scores for the words in this specific row
    row_data = tfidf_matrix.getrow(row_idx).toarray()[0]
    
    # Sort them and grab the top 2 highest scoring words
    top_indices = row_data.argsort()[-2:][::-1] 
    top_words = feature_names[top_indices]
    
    return ", ".join(top_words)

print("Extracting keywords for all incidents... (This takes a few seconds)")
# Apply the function to every row
df['extracted_mo'] = [get_top_keywords(i) for i in range(tfidf_matrix.shape[0])]

print("4. Saving NLP Insights back to the database...")
# Save this clean, structured data into a new table
nlp_df = df[['incident_id', 'extracted_mo']]
nlp_df.to_sql('ai_nlp_insights', conn, if_exists='replace', index=False)

conn.close()
print("Success! NLP has extracted the Modus Operandi for all records.")
print("Example MOs:", df['extracted_mo'].head(5).tolist())