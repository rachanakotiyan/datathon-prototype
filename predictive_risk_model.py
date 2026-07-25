import sqlite3
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import joblib
import warnings

warnings.filterwarnings('ignore')

print("1. Connecting to Database...")
conn = sqlite3.connect('chicago_crime_analytics.db')

# We only need the type of crime, when it happened, and where it happened for this model
query = "SELECT crime_type, timestamp, district FROM crime_incidents"
df = pd.read_sql_query(query, conn)
conn.close()

# Drop any rows with missing data that might crash the AI
df = df.dropna(subset=['timestamp', 'district'])

print("2. Feature Engineering (Prepping Data for AI)...")
# Convert text timestamps into datetime objects so we can extract the hour/day
# Added format='mixed' and errors='coerce' to fix the ValueError with AM/PM parsing
df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed', errors='coerce')

# Drop any rows where the date failed to parse
df = df.dropna(subset=['timestamp'])

df['hour'] = df['timestamp'].dt.hour
df['month'] = df['timestamp'].dt.month
df['day_of_week'] = df['timestamp'].dt.dayofweek

# The AI only understands numbers, so we encode the district names into ID numbers
le_district = LabelEncoder()
df['district_encoded'] = le_district.fit_transform(df['district'].astype(str))

# Define what constitutes a 'High Risk' crime (Target Variable)
high_risk_crimes = ['BATTERY', 'ROBBERY', 'ASSAULT', 'HOMICIDE', 'WEAPONS VIOLATION', 'CRIMINAL SEXUAL ASSAULT']
df['is_high_risk'] = df['crime_type'].apply(lambda x: 1 if x in high_risk_crimes else 0)

# Select our training features (X) and what we are trying to predict (y)
X = df[['hour', 'month', 'day_of_week', 'district_encoded']]
y = df['is_high_risk']

print("3. Training the Random Forest AI Model...")
# Split data: 80% for training, 20% for testing the AI's accuracy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest with 100 'trees'
rf_model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
rf_model.fit(X_train, y_train)

print("4. Evaluating the Model...")
# Ask the AI to predict the 20% of data it hasn't seen yet
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
print("\nDetailed Report:\n", classification_report(y_test, y_pred))

print("5. Saving the AI Brain for the Dashboard...")
# Save the trained model and the district translator so the Dashboard can use them tomorrow
joblib.dump(rf_model, 'predictive_risk_model.pkl')
joblib.dump(le_district, 'district_encoder.pkl')

print("Success! The AI Risk Model is trained and saved to your folder.")