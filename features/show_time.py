import pandas as pd
import joblib
from typing import List
from datetime import timedelta
from datetime import datetime, timedelta

def predicted_hourly_user_activity(events_df: pd.DataFrame, model) -> List[int]:
    """
    Predict hourly user activity using a trained ML model (.pkl).

    Args:
        events_df (pd.DataFrame): Contains 'login_time'
        model: Model to predict the timings

    Returns:
        List[int]: Predicted user logins for each hour (0–23)
    """

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
