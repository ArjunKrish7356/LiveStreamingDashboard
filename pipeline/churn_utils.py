import numpy as np
import pandas as pd
from datetime import timedelta

def find_user_churn_reason(user_id, today, interactions_df, users_df, svm, label_encoder):
    seven_days_ago = today - timedelta(days=7)

    interactions_df["login_time"] = pd.to_datetime(interactions_df["login_time"])
    last_week_df = interactions_df[interactions_df["login_time"] >= seven_days_ago]

    agg_df = last_week_df.groupby("user_id").agg(
        total_watch_time_7d=("total_watch_time", "sum"),
        total_sessions_7d=("user_id", "count"),
        avg_watch_time_per_session_7d=("total_watch_time", "mean"),
        median_pauses_7d=("num_pauses", "median"),
        median_buffer_events_7d=("buffer_events", "median"),
        recommendation_accept_rate_7d=("was_recommended", "mean"),
        genre_diversity_7d=("genres_watched", lambda x: len(set(g for sublist in x for g in eval(sublist))))
    ).reset_index()

    last_session_df = interactions_df.groupby("user_id")["login_time"].max().reset_index()
    last_session_df["days_since_last_session"] = (today - last_session_df["login_time"]).dt.days

    features_df = users_df.merge(agg_df, on="user_id", how="left")
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

    user_values = features_df[features_df['user_id'] == user_id].copy()
    user_values = user_values.drop(columns=[
        'user_id', 'email', 'country', 'registration_date', 
        'preferred_genres', 'subscription_type'
    ])

    # ✅ FIX: pass DataFrame directly instead of reshaped NumPy array
    prediction = svm.predict(user_values)[0]

    # Return decoded label if it exists in encoder
    if isinstance(prediction, (int, float, np.integer)) and prediction in label_encoder.classes_:
        return label_encoder.inverse_transform([prediction])[0]
    else:
        return str(prediction)


def find_all_user_churn_reason(today, interactions_df, users_df, svm, label_encoder):
    churn_reasons = []
    for user_id in users_df["user_id"]:
        reason = find_user_churn_reason(user_id, today, interactions_df, users_df, svm, label_encoder)
        churn_reasons.append(reason)
    return churn_reasons
