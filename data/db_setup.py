import pandas as pd
import os
from . import get_db_connection

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

def init_db():
    conn = get_db_connection()

    # Load CSVs and insert into SQLite
    users_df = pd.read_csv(os.path.join(DATA_DIR, 'users.csv'))
    shows_df = pd.read_csv(os.path.join(DATA_DIR, 'shows.csv'))
    events_df = pd.read_csv(os.path.join(DATA_DIR, 'interactions.csv'))

    users_df.to_sql('users', conn, if_exists='replace', index=False)
    shows_df.to_sql('shows', conn, if_exists='replace', index=False)
    events_df.to_sql('interactions', conn, if_exists='replace', index=False)

    conn.close()