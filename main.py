import streamlit as st
import pandas as pd
import pickle

from ui.churnpage import churnpage
from ui.page2 import page2
from sqlalchemy import create_engine
@st.cache_data
def load_data():
    engine = create_engine("mysql+pymysql://root:@localhost/aiotrix")

    """Load and cache the datasets"""
    shows_df = pd.read_sql("SELECT * FROM shows", engine)
    events_df = pd.read_sql("SELECT * FROM user_sessions_dataset", engine)
    users_df = pd.read_sql("SELECT * FROM users", engine)

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