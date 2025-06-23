from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import pandas as pd

app = FastAPI()
event_csv = pd.read_csv("data/events.csv")

class UserEventData(BaseModel):
    user_id: str
    login_time: datetime
    content_watched: str
    genres_watched: str
    total_watch_time: float
    num_pauses: int
    buffer_events: int
    was_recommended: bool

class UserRegistrationData(BaseModel):
    user_id: str
    email: str
    age: int
    country: str
    registration_date: str
    preferred_genre: str
    subscription_type: str
    churn: str = "no_churn"

@app.post("/register-user")
async def register_user(data: UserRegistrationData):
    # Convert the data to a DataFrame row
    new_row = pd.DataFrame([data.model_dump()])
    
    # Append to the existing CSV (assuming users.csv exists)
    new_row.to_csv("data/users.csv", mode='a', header=False, index=False)
    
    return {"message": "User registered successfully", "data": data}

@app.post("/log-event")
async def add_event_to_datastore(data: UserEventData):
    # Convert the data to a DataFrame row
    new_row = pd.DataFrame([data.model_dump()])
    
    # Append to the existing CSV
    new_row.to_csv("data/events.csv", mode='a', header=False, index=False)
    
    return {"message": "Data received successfully", "data": data}

