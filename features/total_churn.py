import pandas as pd
from datetime import datetime, timedelta

def find_all_user_churn_reason(today, event_df, user_df, model):
    seven_days_ago = today - timedelta(days=7)

    event_df["login_time"] = pd.to_datetime(event_df["login_time"])

    last_week_df = event_df[event_df["login_time"] >= seven_days_ago]

    agg_df = last_week_df.groupby("user_id").agg(
        total_watch_time_7d=("total_watch_time", "sum"),
        total_sessions_7d=("user_id", "count"),
        avg_watch_time_per_session_7d=("total_watch_time", "mean"),
        median_pauses_7d=("num_pauses", "median"),
        median_buffer_events_7d=("buffer_events", "median"),
        recommendation_accept_rate_7d=("was_recommended", "mean"),
        genre_diversity_7d=("genres_watched", lambda x: len(set(g for sublist in x for g in eval(sublist))))
    ).reset_index()


    last_session_df = event_df.groupby("user_id")["login_time"].max().reset_index()
    last_session_df["days_since_last_session"] = (today - last_session_df["login_time"]).dt.days

    features_df = user_df.merge(agg_df, on="user_id", how="left")
    features_df = features_df.merge(last_session_df[["user_id", "days_since_last_session"]], on="user_id", how="left")

    features_df.fillna({
        "total_watch_time_7d": 0,
        "total_sessions_7d": 0,
        "avg_watch_time_per_session_7d": 0,
        "median_pauses_7d": 0,
        "median_buffer_events_7d": 0,
        "recommendation_accept_rate_7d": 0,
        "genre_diversity_7d": 0,
        "days_since_last_session": 999
    }, inplace=True)

    user_values = features_df
    user_values = user_values.drop(columns=['user_id','email','country','registration_date','preferred_genres','subscription_type'])
    hashmap = {
        0: 'bad_recommendation', 
        1: 'genre_fatigue',
        2: 'low_engagement', 
        3: 'no_churn', 
        4: 'poor_user_experience'
    }

    predictions = model.predict(user_values.values)
    return [hashmap[pred] for pred in predictions]