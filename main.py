import streamlit as st
import pandas as pd
import pickle
import os
from sqlalchemy import create_engine

from ui.churnpage import churnpage
from ui.activitypage import activitypage  # renamed page2 -> activitypage

@st.cache_data
def load_data():
    """Load and cache the datasets from MySQL and model from disk."""
    engine = create_engine("mysql+pymysql://root:@localhost/aiotrix")

    shows_df = pd.read_sql("SELECT * FROM shows", engine)
    events_df = pd.read_sql("SELECT * FROM user_sessions_dataset", engine)
    users_df = pd.read_sql("SELECT * FROM users", engine)

    model_path = os.path.join(os.path.dirname(__file__), 'models', 'svm_model_for_churn_v2.pkl')
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    return shows_df, events_df, users_df, model

def main():
    """Main application function"""
    shows_df, events_df, users_df, model = load_data()

    # Wrappers for consistent page loading
    def churn_wrapper():
        return churnpage(events_df, users_df, model)

    def activity_wrapper():
        return activitypage(events_df, users_df, shows_df, model)

    # Define Streamlit navigation pages
    churn_page = st.Page(churn_wrapper, title='Churn Stats', url_path='churn')
    activity_page = st.Page(activity_wrapper, title='User Activity', url_path='activity')

    # Navigation rendering
    pg = st.navigation([churn_page, activity_page])
    pg.run()

if __name__ == '__main__':
    main()
