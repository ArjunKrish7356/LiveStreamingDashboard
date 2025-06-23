import pandas as pd
import joblib
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor

# Load event data
events_df = pd.read_csv('data/events.csv')
events_df['login_time'] = pd.to_datetime(events_df['login_time'])

# Use data from the last 7 days
latest_time = events_df["login_time"].max()
seven_days_ago = latest_time - timedelta(days=7)
recent_df = events_df[events_df["login_time"] >= seven_days_ago].copy()

# Extract features
recent_df['hour'] = recent_df['login_time'].dt.hour
recent_df['dayofweek'] = recent_df['login_time'].dt.dayofweek
recent_df['day'] = recent_df['login_time'].dt.date

# Count logins
login_counts = recent_df.groupby(['day', 'hour', 'dayofweek']).size().reset_index(name='user_logins')

# Prepare data for model
X = login_counts[['hour', 'dayofweek']]
y = login_counts['user_logins']

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model
joblib.dump(model, 'models/user_activity_model.pkl')

print("✅ Model trained and saved to models/user_activity_model.pkl")
