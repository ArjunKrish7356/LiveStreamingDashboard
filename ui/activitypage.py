import streamlit as st
import plotly.graph_objects as go

from features.show_time import predicted_hourly_user_activity
from features.average_watchtime import average_watchtime_for_7_days
from features.top_shows import get_top_watched_shows_last_week

def activitypage(events_df, shows_df):
    """
    This page will have 3 components
     - A graph that shows how many people will arrive in the 24 hours. Each hour will have its own vertical line. Use color green for all. This will be in the top left corner
     - A line that shows total average watchtime. The x axis should be the dates from the tuple and y axis should be time in minutes. Use red color for line. This is in top right.
     - A table that uses function get_top_watched_shows_last_week to shows the top watched shows. 2 columns, show name and genres( the fucntion will return list of genres). This is in bottom full span
    
    """
    # Set page to wide mode
    st.set_page_config(layout="wide",)
    
    st.title("User Activity Dashboard")
    
    # Create top row with two columns
    top_left, top_right = st.columns(2)
    
    with top_left:
        # Top left: Hourly prediction graph
        hourly_data = predicted_hourly_user_activity(events_df)
        
        fig1 = go.Figure(data=[
            go.Bar(
                x=list(range(1,25)),
                y=hourly_data,
                marker_color='green',
                name='Predicted Users'
            )
        ])
        
        fig1.update_layout(
            title="Predicted Hourly User Activity",
            xaxis_title="Hour of Day",
            yaxis_title="Number of Users",
            xaxis=dict(
                tickmode='linear', 
                dtick=1,
                tickangle=0  # Keep x-axis labels horizontal
            ),
            showlegend=False
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with top_right:
        # Top right: Average watchtime line chart
        watchtime_data = average_watchtime_for_7_days(events_df)
        
        fig2 = go.Figure(data=[
            go.Scatter(
                x=[item[0] for item in watchtime_data],
                y=[item[1] for item in watchtime_data],
                mode='lines+markers',
                line=dict(color='red'),
                name='Average Watchtime'
            )
        ])
        
        fig2.update_layout(
            title="7-Day Average Watchtime",
            xaxis_title="Date",
            yaxis_title="Time (minutes)",
            showlegend=False
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # Bottom: Top shows table (80% width)
    st.subheader("Top Watched Shows")
    
    # Create columns for centering the table
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
    
    with col2:
        top_shows = get_top_watched_shows_last_week(events_df, shows_df)
        
        # Format data for display
        show_data = []
        for show in top_shows:
            print(show)
            show_data.append({
                "Show Name": show[0],
                "Genres": ", ".join(show[1])
            })
        
        st.dataframe(show_data, use_container_width=True)