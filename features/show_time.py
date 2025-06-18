import pandas as pd
from datetime import datetime, timedelta
from typing import List

def predicted_hourly_user_activity(events_df: pd.DataFrame) -> List[float]:
    """
    Returns a list of predicted average number of users expected to log in each hour
    of the day based on login activity from the last 7 days.

    Args:
        events_df: pandas DataFrame with at least a 'login_time' column

    Returns:
        List of 24 values representing the average user logins for each hour (0 to 23)
    """
    events_df['login_time'] = pd.to_datetime(events_df['login_time'])

    # Get the most recent date in the dataset
    latest_time = events_df["login_time"].max()
    today = latest_time.normalize()
    seven_days_ago = today - timedelta(days=7)

    # Filter for last 7 days
    recent_df = events_df[events_df["login_time"] >= seven_days_ago].copy()
    recent_df["hour"] = recent_df["login_time"].dt.hour

    # Count logins per hour across the 7 days
    hourly_counts = recent_df.groupby("hour")["user_id"].count()

    # Average per hour (normalize across 7 days)
    hourly_average = [hourly_counts.get(hour, 0) / 7 for hour in range(24)]

    return hourly_average
