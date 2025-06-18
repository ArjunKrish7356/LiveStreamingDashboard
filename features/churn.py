from typing import Any, List, Tuple
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine

def total_and_categorial_churn(model) -> Tuple[float, List[Tuple[int, str]]]:
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
    engine = create_engine("mysql+pymysql://root:@localhost/Aiotrix")
    users_df = pd.read_sql("SELECT * FROM users", engine)
    event_df = pd.read_sql("SELECT * FROM user_sessions_dataset", engine)

    today = datetime(2025, 6, 6)
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

    user_values = features_df
    user_values = user_values.drop(columns=['user_id','email','country','registration_date','preferred_genres','subscription_type'])
    predictions = model.predict(user_values)

    # Calculate total churn percentage and list of (user_id, churn_reason)
    churned_users = []
    churn_count = 0

    for idx, prediction in enumerate(predictions):
        if prediction != 'no_churn':
            user_id = features_df.iloc[idx]["user_id"]
            churned_users.append((user_id, prediction))
            churn_count += 1

    churn_percentage = churn_count / len(features_df) if len(features_df) > 0 else 0.0

    return churn_percentage, churned_users

    


