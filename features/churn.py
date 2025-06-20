from typing import Any, List, Tuple
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st

def total_and_categorial_churn(event_df, users_df, churn_model, churn_reason_model) -> Tuple[float, List[Tuple[int, str]]]:
    """
    A function that return total churn percentage from total no of people and also a list containing no
    people in risk of churn in each category

    Args:
        event_df: pandas object containing interactions data
        user_df: pandas object containing users data
        model: A pre-trained model (e.g., SVM) for churn prediction

    Result:
        percentage of people in risk of churn from total people ( between 0 and 1)
        list[(userid, reason)]
    """
    event_df["login_time"] = pd.to_datetime(event_df["login_time"])
    today = event_df["login_time"].max()
    seven_days_ago = today - timedelta(days=7)
    last_week_df = event_df[event_df["login_time"] >= seven_days_ago]

    agg_df = last_week_df.groupby("user_id").agg(
        total_watch_time_7d=("total_watch_time", "sum"),
        total_sessions_7d=("user_id", "count"),
        avg_watch_time_per_session_7d=("total_watch_time", "mean"),
        median_pauses_7d=("num_pauses", "median"),
        median_buffer_events_7d=("buffer_events", "median"),
        recommendation_accept_rate_7d=("was_recommended", "mean"),
        genre_diversity_7d=("genres_watched", lambda x: len(set(x)))
    ).reset_index()

    last_session_df = event_df.groupby("user_id")["login_time"].max().reset_index()
    last_session_df["days_since_last_session"] = (today - last_session_df["login_time"]).dt.days

    final_features_df = pd.merge(agg_df, last_session_df, on="user_id", how="left")
    
    # Drop columns not needed for prediction
    prediction_features = final_features_df.drop(columns=['user_id','login_time'])

    @st.cache_data
    def get_churn_predictions(prediction_features):
        return churn_model.predict(prediction_features.values)

    churn_predictions = get_churn_predictions(prediction_features)

    # Calculate total churn percentage and list of (user_id, churn_reason)
    churned_users = []
    churn_count = 0

    for idx, prediction in enumerate(churn_predictions):
        if prediction == 1:
            user_id = agg_df.iloc[idx]["user_id"]
            # Get features for this user and predict churn reason
            user_features = prediction_features.iloc[idx:idx+1]
            churn_reason = churn_reason_model.predict(user_features)[0]
            churned_users.append((user_id, churn_reason))
            churn_count += 1

    churn_percentage = round(churn_count / len(prediction_features), 2) if len(prediction_features) > 0 else 0.0

    return (int(churn_percentage*100))/100, churned_users


