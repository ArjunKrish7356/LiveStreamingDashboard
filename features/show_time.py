import pandas as pd
import joblib
from typing import List
from datetime import timedelta
from datetime import datetime, timedelta

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

    # Predict for "today" (or next day), across all 24 hours
    today = datetime.now()
    dayofweek = today.weekday()  # Monday=0, Sunday=6

    # Prepare feature input: hours 0 to 23 for today
    features = pd.DataFrame({
        'hour': list(range(24)),
        'dayofweek': [dayofweek] * 24
    })

    # Predict
    predictions = model.predict(features)

    # Return rounded predictions
    return [int(round(pred)) for pred in predictions]
