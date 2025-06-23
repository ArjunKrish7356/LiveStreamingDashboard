# LiveStreamingDashboard

An adaptive engagement intelligence platform for live streaming. This project provides a comprehensive solution for live streaming platforms to analyze viewer behavior, predict engagement, and optimize the streaming experience in real-time.

<!-- Placeholder for a project demo video -->
https://github.com/user-attachments/assets/746fdcfb-96d2-4aac-81db-71e2b99be5e1

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Running the Backend](#running-the-backend)
  - [Running the Frontend](#running-the-frontend)
- [API Endpoints](#api-endpoints)
  - [Register User](#register-user)
  - [Log Event](#log-event)

## Features
- **FastAPI Backend**: A robust server to log event and user data seamlessly.
- **Streamlit Frontend**: A two-page interactive dashboard for data visualization and analysis.
- **Churn Prediction**:
    - Utilizes a machine learning pipeline with Logistic Regression to predict user churn.
    - Employs a RandomForest model to identify the underlying reasons for churn.
    - Visualizes churn probability, reason distribution, and user-specific churn insights.
- **User Activity Analytics**:
    - Tracks and displays average user watch time per day.
    - Presents a weekly summary of top-viewed shows.
    - Forecasts hourly user traffic for the next 24 hours using a RandomForest model based on the past week's data.

## Project Structure
The project is organized into the following directories:
- `main.py`: The entry point for the Streamlit application, integrating all components.
- `server.py`: The FastAPI backend server for handling API requests.
- `data/`: Stores the datasets, including `users.csv`, `events.csv`, and `shows.csv`.
- `features/`: Contains feature engineering scripts (`average_watchtime.py`, `churn.py`, `show_time.py`, `top_shows.py`).
- `models/`: Contains serialized machine learning models for prediction.
- `ui/`: Holds the Streamlit components for the `activitypage.py` and `churnpage.py`.

## Getting Started

### Prerequisites
- Python 3.13.3
- Git

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/ArjunKrish7356/LiveStreamingDashboard.git
   cd LiveStreamingDashboard
   ```
2. **Run the initialization script:**
   This script will create a virtual environment and install the required dependencies.
   ```bash
   ./initialisation.sh
   ```

## Usage
The application consists of a backend server and a frontend dashboard, which must be run in separate terminals.

### Running the Backend
To start the FastAPI server, run the following command:
```bash
fastapi run server.py
```
The backend API will be available at `http://127.0.0.1:8000`.

### Running the Frontend
To launch the Streamlit dashboard, run:
```bash
streamlit run main.py
```
The frontend will be available at `http://localhost:8501`.

## API Endpoints

### Register User
- **Endpoint**: `/register-user`
- **Method**: `POST`
- **Description**: Registers a new user in the system.
- **Payload**:
  ```json
  {
    "user_id": "string",
    "email": "string",
    "age": "integer",
    "country": "string",
    "registration_date": "string",
    "preferred_genre": "string",
    "subscription_type": "string"
  }
  ```

### Log Event
- **Endpoint**: `/log-event`
- **Method**: `POST`
- **Description**: Logs a new user event.
- **Payload**:
  ```json
  {
    "user_id": "string",
    "login_time": "datetime",
    "content_watched": "string",
    "genres_watched": "string",
    "total_watch_time": "float",
    "num_pauses": "integer",
    "buffer_events": "integer",
    "was_recommended": "boolean"
  }
  ```
