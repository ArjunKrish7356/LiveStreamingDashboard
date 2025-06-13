import pandas as pd

def find_average_watchtime_for_a_date(date, event_df):
    event_df["login_time"] = pd.to_datetime(event_df["login_time"])

    filtered_df = event_df[event_df['login_time'].dt.date == date]
    return filtered_df