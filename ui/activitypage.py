import streamlit as st
import pandas as pd
import io
import base64
import plotly.graph_objects as go
from features.Corelation import generate_model_input_features, get_correlation_heatmap
from features.show_time import predicted_hourly_user_activity
from features.average_watchtime import average_watchtime_for_7_days
from features.top_shows import get_top_watched_shows_last_week

def activitypage(event_df: pd.DataFrame, users_df: pd.DataFrame, shows_df: pd.DataFrame, model):
    st.set_page_config(layout="wide")
    st.title("📊 User Activity & Churn Analysis Dashboard")

    # === Top Row with Hourly Activity & Average Watchtime ===
    top_left, top_right = st.columns(2)

    with top_left:
        st.subheader("Predicted Hourly User Activity")
        hourly_data = predicted_hourly_user_activity(event_df)

        fig1 = go.Figure(data=[
            go.Bar(
                x=list(range(1, 25)),
                y=hourly_data,
                marker_color='green'
            )
        ])
        fig1.update_layout(
            xaxis_title="Hour of Day",
            yaxis_title="Number of Users",
            xaxis=dict(tickmode='linear', dtick=1),
            showlegend=False
        )
        st.plotly_chart(fig1, use_container_width=True)

    with top_right:
        st.subheader("7-Day Average Watchtime")
        watchtime_data = average_watchtime_for_7_days(event_df)
        fig2 = go.Figure(data=[
            go.Scatter(
                x=[item[0] for item in watchtime_data],
                y=[item[1] for item in watchtime_data],
                mode='lines+markers',
                line=dict(color='red')
            )
        ])
        fig2.update_layout(
            xaxis_title="Date",
            yaxis_title="Time (minutes)",
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)

    # === Middle Row: Churn Correlation Heatmap ===
    st.subheader("Correlation Heatmap with Churn")
    with st.spinner("Generating churn heatmap..."):
        df = generate_model_input_features(event_df, users_df)
        model_input = df.drop(columns=[
            'user_id', 'email', 'country', 'registration_date',
            'preferred_genres', 'subscription_type'
        ], errors='ignore')

        df['churn_flag'] = model.predict(model_input)
        df['churn_flag'] = df['churn_flag'].apply(lambda x: 1 if x != 'no_churn' else 0)

        columns_to_plot = model_input.columns.tolist() + ['churn_flag']
        base64_img = get_correlation_heatmap(df, columns_to_plot)
        st.image(io.BytesIO(base64.b64decode(base64_img)), use_column_width=True)

    # === Bottom Row: Top Watched Shows Table ===
    st.subheader("Top Watched Shows")
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
    with col2:
        top_shows = get_top_watched_shows_last_week(event_df, shows_df)
        table_data = [
            {"Show Name": show[0], "Genres": ", ".join(show[1])}
            for show in top_shows
        ]
        st.dataframe(table_data, use_container_width=True)
