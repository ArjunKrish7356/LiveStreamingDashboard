# LiveStreamingDashboard

An adaptive engagement intelligence platform for live streaming. This project provides a comprehensive solution for live streaming platforms to analyze viewer behavior, predict engagement, and optimize the streaming experience in real-time.

(I will add a video of its working here)

## What it does:
- A FastAPI server to log event-data and user-data.
- A 2-page frontend created with Streamlit.
- The first page shows churn statistics calculated using a pipeline of two advanced ML models. The first model, a logistic regression model, predicts whether a user will churn. The second, a RandomForest model, determines the reason for the churn. This page displays the percentage of users likely to churn, a chart showing the ratio of users likely to churn for each reason, and a table with user IDs and their churn reasons.
- The second page displays user activity statistics, including the average user watch time per day and a table of the top-viewed shows in the past week. It also uses a RandomForest ML model to predict the number of users expected each hour for the next 24 hours by analyzing the past week's data.

## Folder Organization
- **data/**: Contains `events.csv` to store event data, `users.csv` to store user data, and `shows.csv` to store show data.
- **features/**: Contains functions for calculations: `average_watchtime.py`, `churn.py`, `show_time.py`, and `top_shows.py`.
- **models/**: Contains models to predict churn, churn reason, and the number of people that might come in the coming hours.
- **ui/**: Contains the UI for the activity and churn pages, built with Streamlit.
- **main.py**: Combines the UI, data, features, and models to make everything work.
- **server.py**: Contains the FastAPI code to run the backend for logging events and user data.

## How to start
After cloning the repo, first run `initialisation.sh`. It will set up the required dependencies and the virtual environment.

## To run UI
Run `streamlit run main.py` to start the frontend. It will be available at `http://localhost:8501`.

## To run backend
Type in a new terminal `fastapi run server.py`.

### Endpoints
- **`/register-user`**: Registers a new user.
  - **Input structure**:
    - `user_id`: string
    - `email`: string
    - `age`: integer
    - `country`: string
    - `registration_date`: string
    - `preferred_genre`: string
    - `subscription_type`: string
- **`/log-event`**: Logs an event.
  - **Input structure**:
    - `user_id`: string
    - `login_time`: datetime
    - `content_watched`: string
    - `genres_watched`: string
    - `total_watch_time`: float
    - `num_pauses`: integer
    - `buffer_events`: integer
    - `was_recommended`: boolean