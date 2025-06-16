import pandas as pd
from datetime import datetime, timedelta
from typing import List

def average_watchtime_for_7_days(event_df) -> List[float]:
    """
    Returns a list containing the average watch time for each of the past 7 days.

    Args:
        event_df: pandas DataFrame with at least 'login_time' and 'total_watch_time' columns

    Returns:
        List of average watch times for each of the last 7 days (index 0 = 6 days ago, index 6 = today)
    """
    event_df["login_time"] = pd.to_datetime(event_df["login_time"])
    today = event_df["login_time"].max().date()
    averages = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_df = event_df[event_df['login_time'].dt.date == day]
        avg_watch_time = float(day_df['total_watch_time'].mean()) if not day_df.empty else 0
        averages.append(avg_watch_time)

    return averages

