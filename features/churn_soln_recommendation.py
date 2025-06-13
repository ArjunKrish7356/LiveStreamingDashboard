import pandas as pd
from datetime import datetime, timedelta
from total_churn import find_all_user_churn_reason

def recommend_top_10_shows(today, event_df, user_df, movies_df, model):
    """
    Recommend top 10 shows for churned users based on churn reason and preferences.

    Args:
        today (datetime): Current date.
        event_df (pd.DataFrame): User event data.
        user_df (pd.DataFrame): User profile data.
        movies_df (pd.DataFrame): Movies/shows metadata.
        model: Trained churn prediction model.

    Returns:
        list: Top 10 recommended show titles (str), in order.
    """

    churn_reasons = find_all_user_churn_reason(today, event_df, user_df, model)
    result_df = user_df[["user_id", "preferred_genres"]].copy()
    result_df["churn_reason"] = churn_reasons
    churned_users = result_df[result_df["churn_reason"] != "no_churn"].copy()

    recommended_titles = []

    for _, row in churned_users.iterrows():
        user_id = row["user_id"]
        churn_reason = row["churn_reason"]
        preferred_genres = eval(row["preferred_genres"]) if isinstance(row["preferred_genres"], str) else row["preferred_genres"]

        seven_days_ago = today - timedelta(days=7)
        user_sessions = event_df[(event_df["user_id"] == user_id) &
                                 (pd.to_datetime(event_df["login_time"]) >= seven_days_ago)]
        recent_genres = set()
        for genres in user_sessions["genres_watched"].apply(eval):
            recent_genres.update(genres)

        if churn_reason == "genre_fatigue":
            new_genres = [g for g in movies_df["genre"].unique() if g not in recent_genres]
            rec_movies = movies_df[movies_df["genre"].isin(new_genres)]["title"].tolist()

        elif churn_reason == "bad_recommendation":
            rec_movies = movies_df[movies_df["genre"].isin(preferred_genres)]["title"].tolist()

        elif churn_reason == "poor_user_experience":
            rec_movies = movies_df["title"].tolist()

        elif churn_reason == "low_engagement":
            rec_movies = movies_df[movies_df["genre"].isin(preferred_genres)]["title"].tolist()

        else:
            rec_movies = []

        recommended_titles.extend(rec_movies)

    # Remove duplicates while preserving order
    seen = set()
    top_10 = []
    for title in recommended_titles:
        if title not in seen:
            seen.add(title)
            top_10.append(title)
        if len(top_10) == 10:
            break

    return top_10

# Example usage:
# today = datetime(2025, 6, 6)
# event_df = pd.read_csv("interactions.csv")
# user_df = pd.read_csv("users.csv")
# movies_df = pd.read_csv("movies.csv")
# model = ... # Load or define your churn prediction model
# top_10_shows = recommend_top_10_shows(today, event_df, user_df, movies_df, model)
# print(top_10_shows)