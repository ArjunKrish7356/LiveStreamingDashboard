import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import io
import base64

from features.show_time import predicted_hourly_user_activity
from features.average_watchtime import average_watchtime_for_7_days
from features.top_shows import get_top_watched_shows_last_week
from features.Corelation import generate_model_input_features, get_correlation_heatmap

def activitypage(events_df, shows_df, users_df, model):
    st.set_page_config(layout="wide")
    st.title("📈 User Activity Dashboard")

    # Top graphs
    top_left, top_right = st.columns(2)

    with top_left:
        hourly_data = predicted_hourly_user_activity(events_df)
        fig1 = go.Figure([
            go.Bar(x=list(range(1, 25)), y=hourly_data, marker_color='green')
        ])
        fig1.update_layout(
            title="Predicted Hourly User Activity",
            xaxis_title="Hour of Day",
            yaxis_title="Number of Users",
            xaxis=dict(tickmode='linear', dtick=1),
            showlegend=False
        )
        st.plotly_chart(fig1, use_container_width=True)

    with top_right:
        watchtime_data = average_watchtime_for_7_days(events_df)
        fig2 = go.Figure([
            go.Scatter(
                x=[item[0] for item in watchtime_data],
                y=[item[1] for item in watchtime_data],
                mode='lines+markers',
                line=dict(color='red')
            )
        ])
        fig2.update_layout(
            title="7-Day Average Watchtime",
            xaxis_title="Date",
            yaxis_title="Time (minutes)",
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Correlation heatmap
    st.subheader("🔍 Correlation with Churn")
    with st.spinner("Generating churn heatmap..."):
        df = generate_model_input_features(events_df, users_df)
        model_input = df.drop(columns=[
            'user_id', 'email', 'country', 'registration_date',
            'preferred_genres', 'subscription_type'
        ], errors='ignore')

        df['churn_flag'] = model.predict(model_input)
        df['churn_flag'] = df['churn_flag'].apply(lambda x: 1 if x != 'no_churn' else 0)

        columns_to_plot = model_input.columns.tolist() + ['churn_flag']
        base64_img = get_correlation_heatmap(df, columns_to_plot)
        st.image(io.BytesIO(base64.b64decode(base64_img)), use_column_width=True)

    # Top shows table
    st.subheader("🎬 Top Watched Shows")
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
    with col2:
        top_shows = get_top_watched_shows_last_week(events_df, shows_df)
        show_data = [{"Show Name": show[0], "Genres": ", ".join(show[1])} for show in top_shows]
        st.dataframe(show_data, use_container_width=True)
