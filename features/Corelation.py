import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

def generate_model_input_features(event_df: pd.DataFrame, users_df: pd.DataFrame) -> pd.DataFrame:
    from datetime import datetime, timedelta

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

    # Fill NA values
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

    return features_df

def prepare_user_features(event_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate session-level data into user-level features."""
    agg_df = event_df.groupby('user_id').agg({
        'total_watch_time': 'mean',
        'num_pauses': 'mean',
        'buffer_events': 'mean',
        'was_recommended': 'mean'
    }).reset_index()

    return agg_df

def predict_churn_and_flag(user_df: pd.DataFrame, model) -> pd.DataFrame:
    """Use model to predict churn and add a churn_flag column."""
    X = user_df.drop(columns=['user_id'])
    user_df['churn_flag'] = model.predict(X)
    user_df['churn_flag'] = user_df['churn_flag'].apply(lambda x: 1 if x != 'no_churn' else 0)
    return user_df

def get_correlation_heatmap(df: pd.DataFrame, columns: list) -> str:
    """Generate a base64 heatmap image of correlation matrix."""
    corr = df[columns].corr()

    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix with Churn", fontsize=14)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    plt.close()

    return image_base64

def page2(event_df: pd.DataFrame, model):
    """Streamlit page to show correlation matrix."""
    st.title("📊 Churn Correlation Analysis")

    with st.spinner("Preparing correlation heatmap..."):
        user_df = prepare_user_features(event_df)
        user_df = predict_churn_and_flag(user_df, model)

        columns = [
            'total_watch_time',
            'num_pauses',
            'buffer_events',
            'was_recommended',
            'churn_flag'
        ]

        image_base64 = get_correlation_heatmap(user_df, columns)
        st.subheader("Correlation Heatmap")
        st.image(io.BytesIO(base64.b64decode(image_base64)), use_column_width=True)
