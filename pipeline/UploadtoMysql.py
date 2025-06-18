import os
import pandas as pd
from sqlalchemy import create_engine

# DB config
DB_USER = "root"
DB_PASSWORD = ""  
DB_HOST = "localhost"
DB_NAME = "Aiotrix" 

# Create SQLAlchemy engine
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")


data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')

for file_name in os.listdir(data_folder):
    if file_name.endswith('.csv'):
        file_path = os.path.join(data_folder, file_name)
        table_name = os.path.splitext(file_name)[0]  

        print(f"Uploading {file_name} as table '{table_name}'...")
        df = pd.read_csv(file_path)
        df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

print("All CSV files uploaded to MySQL!")
