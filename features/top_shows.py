import pandas as pd
from datetime import timedelta
from collections import defaultdict
from typing import List, Tuple

def get_top_watched_shows_last_week(event_df: pd.DataFrame, shows_df: pd.DataFrame) -> List[Tuple[str, List[str]]]:
    """
    Returns a list of the top 10 watched shows from the last 7 days, with show name and genre.

    Args:
        event_df (pd.DataFrame): DataFrame with event data, including 'login_time' and 'content_watched'.
        shows_df (pd.DataFrame): DataFrame with show metadata including 'show_id', 'show_name', and 'genre'.

    Returns:
        List[Tuple[str, List[str]]]: Top 10 (show_name, [genre]) pairs, sorted by watch count.
    """

    # Ensure datetime conversion
    event_df['login_time'] = pd.to_datetime(event_df['login_time'])

    # Filter data to last 7 days
    now = event_df['login_time'].max()
    last_week = now - timedelta(days=7)
    recent_events = event_df[event_df['login_time'] >= last_week]

    # Count how often each show appears
    show_counts = defaultdict(int)
    for shows in recent_events['content_watched']:
        if isinstance(shows, str):
            try:
                show_list = eval(shows)
            except Exception:
                continue
        else:
            show_list = shows

        for show_id in show_list:
            show_counts[show_id] += 1

    # Sort show_ids by view count and get top 10
    top_show_ids = sorted(show_counts, key=show_counts.get, reverse=True)[:10]

    # Construct list of (show_name, [genre]) for top 10
    top_shows = []
    for show_id in top_show_ids:
        match = shows_df[shows_df['show_id'] == show_id]
        if not match.empty:
            show_name = match['show_name'].iloc[0]
            genre = match['genre'].iloc[0]
            top_shows.append((show_name, [genre]))

    return top_shows
