import streamlit as st
import pandas as pd
import pickle

from ui.churnpage import churnpage
from ui.activitypage import activitypage

@st.cache_data
def load_data():
    """Load and cache the datasets"""
    shows_df = pd.read_csv('data/shows.csv')
    events_df = pd.read_csv('data/user_sessions_dataset.csv')
    users_df = pd.read_csv('data/users.csv')
    with open('models/svm_model_for_churn_v2.pkl', 'rb') as f:
        model = pickle.load(f)
    return shows_df, events_df, users_df, model

def main():
    """Main application function"""
    # Load cached data
    shows_df, events_df, users_df, model= load_data()
    
    def churn_wrapper():
        return churnpage(events_df, users_df, model)
    
    def activity_wrapper():
        return activitypage(events_df, shows_df)
    
    churn_page = st.Page(churn_wrapper, title='Churn Stats', url_path='churn')
    activity_page = st.Page(activity_wrapper, title='User Activity', url_path='activity')

    pg = st.navigation([churn_page, activity_page])
    pg.run()
    
if __name__ == '__main__':
    main()