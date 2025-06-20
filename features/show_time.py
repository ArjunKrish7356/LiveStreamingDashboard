import pandas as pd
from datetime import datetime, timedelta
from typing import List

def predicted_hourly_user_activity(events_df: pd.DataFrame) -> List[int]:
    """
    Returns a list of predicted number of users expected to log in each hour
    of the day based on login activity from the last 7 days.

    Args:
        events_df: pandas DataFrame with at least a 'login_time' column (which contains full timestamps)

    Returns:
        List of 24 integer values representing the predicted user logins for each hour (0 to 23)
    """
    # Use logout_time since it contains the actual hour information
    events_df['login_time'] = pd.to_datetime(events_df['login_time'])

    # Get the most recent date in the dataset
    latest_time = events_df["login_time"].max()
    today = latest_time.normalize()
    seven_days_ago = today - timedelta(days=7)

    # Filter for last 7 days
    recent_df = events_df[events_df["login_time"] >= seven_days_ago].copy()
    recent_df["hour"] = recent_df["login_time"].dt.hour
    recent_df["date"] = recent_df["login_time"].dt.date

    # Count logins per hour per day, then calculate median across days
    daily_hourly_counts = recent_df.groupby(["date", "hour"])["user_id"].count().reset_index()
    
    # Calculate median for each hour across all days
    hourly_medians = daily_hourly_counts.groupby("hour")["user_id"].median()
    
    # Get median predictions for each hour (0-23), defaulting to 0 if no data
    hourly_predictions = [int(round(hourly_medians.get(hour, 0))) for hour in range(24)]

    return hourly_predictions