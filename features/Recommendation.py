import pandas as pd
from datetime import datetime, timedelta
import joblib
import sys
import os

# Dynamically resolve project root and set data/model paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")

sys.path.append(BASE_DIR)

from pipeline.churn_utils import find_all_user_churn_reason

# === Load Model and Label Encoder ===
svm = joblib.load(os.path.join(MODEL_DIR, "svm_model_for_churn_v2.pkl"))
label_encoder = joblib.load(os.path.join(MODEL_DIR, "label_encoder.pkl"))

def recommend_shows_for_churned_users(today, event_df, user_df, shows_file):
    if not os.path.exists(shows_file):
        raise FileNotFoundError(f"⚠️ shows.csv not found at: {shows_file}")

    shows_df = pd.read_csv(shows_file)

    churn_reasons = find_all_user_churn_reason(today, event_df, user_df, svm, label_encoder)

    result_df = user_df[["user_id", "preferred_genres"]].copy()
    result_df["churn_reason"] = churn_reasons

    churned_users = result_df[result_df["churn_reason"] != "no_churn"].copy()
    churned_users["recommended_shows"] = ""

    for idx, row in churned_users.iterrows():
        user_id = row["user_id"]
        churn_reason = row["churn_reason"]
        preferred_genres = eval(row["preferred_genres"])

        seven_days_ago = today - timedelta(days=7)
        user_sessions = event_df[
            (event_df["user_id"] == user_id) & 
            (pd.to_datetime(event_df["login_time"]) >= seven_days_ago)
        ]

        recent_genres = set()
        for genres in user_sessions["genres_watched"].apply(eval):
            recent_genres.update(genres)

        if churn_reason == "genre_fatigue":
            new_genres = [g for g in shows_df["genre"].unique() if g not in recent_genres]
            rec_shows = shows_df[shows_df["genre"].isin(new_genres)]["show_name"].head(2).tolist()
        elif churn_reason == "bad_recommendation":
            rec_shows = shows_df[shows_df["genre"].isin(preferred_genres)]["show_name"].head(2).tolist()
        elif churn_reason == "poor_user_experience":
            rec_shows = shows_df[shows_df["duration"] < 60]["show_name"].head(2).tolist()
        elif churn_reason == "low_engagement":
            rec_shows = shows_df[
                (shows_df["genre"].isin(preferred_genres)) &
                (shows_df["ratings"] >= 4.0)
            ]["show_name"].head(2).tolist()
        else:
            rec_shows = []

        churned_users.at[idx, "recommended_shows"] = ", ".join(rec_shows) if rec_shows else "None"

    return churned_users[["user_id", "churn_reason", "recommended_shows"]]

# === Run Recommendation ===
if __name__ == "__main__":
    today = datetime(2025, 6, 6)

    interactions_path = os.path.join(DATA_DIR, "user_sessions_dataset.csv")
    users_path = os.path.join(DATA_DIR, "users.csv")
    shows_path = os.path.join(DATA_DIR, "shows.csv")
    output_path = os.path.join(DATA_DIR, "output", "churn_recommendations.csv")

    interactions_df = pd.read_csv(interactions_path)
    users_df = pd.read_csv(users_path)

    recommendations_df = recommend_shows_for_churned_users(today, interactions_df, users_df, shows_path)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    recommendations_df.to_csv(output_path, index=False)

    print(recommendations_df.to_markdown(index=False))
