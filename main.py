# database/db_debug.py
from data import get_db_connection
from data.db_setup import init_db
from features.top_shows import get_top_watched_shows_last_week
import pickle
import pandas as pd

if __name__ == "__main__":
    model = pickle.load(open('models/svm_model_for_churn_v2.pkl', 'rb'))  # Load your model here
    event_df = pd.read_csv('data/user_sessions_dataset.csv')
    users_df = pd.read_csv('data/users.csv')
    shows_df = pd.read_csv('data/shows.csv')
    print(get_top_watched_shows_last_week(event_df, shows_df))