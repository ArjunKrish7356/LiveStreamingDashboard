import pandas as pd
from ast import literal_eval
from collections import Counter

def get_users_who_watched_top_shows(interactions_df, last_week_df, top_n=10):
    # Ensure 'content_watched' is a list
    interactions_df = interactions_df.copy()
    interactions_df["content_watched"] = interactions_df["content_watched"].apply(literal_eval)

    # Flatten all shows and count
    all_shows = [show for sublist in interactions_df["content_watched"] for show in sublist]
    show_counts = Counter(all_shows)
    top_n_shows = [show for show, _ in show_counts.most_common(top_n)]

    # Function to check if any top show was watched
    def watched_top_show(row):
        try:
            shows = set(literal_eval(row))
            return int(any(show in top_n_shows for show in shows))
        except Exception:
            return 0

    # Apply to last_week_df
    last_week_df = last_week_df.copy()
    last_week_df["watched_top_show"] = last_week_df["content_watched"].apply(watched_top_show)

    # Aggregate per user
    watched_top_flag = last_week_df.groupby("user_id")["watched_top_show"].max().reset_index()
    return watched_top_flag
