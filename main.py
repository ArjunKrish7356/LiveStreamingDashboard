import streamlit as st
import pandas as pd
import pickle

from ui.churnpage import churnpage
from ui.page2 import page2

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
    
    churn_page = st.Page(churnpage(events_df, users_df, model), title='Churn Stats')
    page23 = st.Page(page2, title='page2')

    pg = st.navigation([churn_page, page23])
    st.sidebar.markdown("# Main page 🎈")
    pg.run()

if __name__ == '__main__':
    main()