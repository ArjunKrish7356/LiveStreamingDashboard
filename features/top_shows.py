import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict

from typing import List

def get_top_watched_shows_last_week(event_df, shows_df) -> List[str]:
    """
    Returns a list of the top watched shows from the last 7 days.

    Args:
        event_df (pd.DataFrame): DataFrame containing event data.
        shows_df (pd.DataFrame): DataFrame containing show details.

    Returns:
        list: Top watched shows in descending order (most watched at index 0).
    """

    # Convert login_time to datetime objects
    event_df['login_time'] = pd.to_datetime(event_df['login_time'])

    # Filter events from the last 7 days
    now = event_df['login_time'].max()
    last_week = now - timedelta(days=7)
    recent_events = event_df[event_df['login_time'] >= last_week]

    # Create a hashmap (dictionary) to count occurrences of each show
    show_counts = defaultdict(int)

    # Count how many times each show was watched
    for shows in recent_events['content_watched']:
        # If shows is a string, try to eval or parse it as a list
        if isinstance(shows, str):
            try:
                show_list = eval(shows)
            except Exception:
                continue
        else:
            show_list = shows
        for show in show_list:
            show_counts[show] += 1

    # Sort shows by count in descending order
    top_shows = sorted(show_counts, key=show_counts.get, reverse=True)
    
    show_names = []
    for show_id in top_shows:
        show_name_row = shows_df[shows_df['show_id'] == show_id]['show_name'].iloc[0]
        show_names.append(show_name_row)
    return show_names