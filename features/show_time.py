import pandas as pd
import joblib
from typing import List
from datetime import timedelta

def predicted_hourly_user_activity(events_df: pd.DataFrame) -> List[int]:
    """
    Predict hourly user activity using a trained ML model (.pkl).

    Args:
        events_df (pd.DataFrame): Contains 'login_time'

    Returns:
        List[int]: Predicted user logins for each hour (0–23)
    """

    # Load trained model
    model = joblib.load('models/user_activity_model.pkl')

    # Preprocess data to create features
    events_df['login_time'] = pd.to_datetime(events_df['login_time'])
    latest_time = events_df['login_time'].max()
    last_week = latest_time - timedelta(days=7)

    recent_df = events_df[events_df['login_time'] >= last_week].copy()
    recent_df['hour'] = recent_df['login_time'].dt.hour
    recent_df['dayofweek'] = recent_df['login_time'].dt.dayofweek

    # Group and count user logins for model input
    grouped = recent_df.groupby(['dayofweek', 'hour'])['user_id'].count().reset_index()
    grouped.rename(columns={'user_id': 'logins'}, inplace=True)

    # Generate predictions for each hour (0–23)
    predictions = []
    for hour in range(24):
        # Example: Use average across all weekdays for this hour
        hour_data = grouped[grouped['hour'] == hour]
        avg_logins = hour_data['logins'].mean() if not hour_data.empty else 0

        # Create feature row to predict (you’ll adjust this based on your model)
        feature = [[hour, avg_logins]]
        pred = model.predict(feature)[0]
        predictions.append(int(round(pred)))

    return predictions
