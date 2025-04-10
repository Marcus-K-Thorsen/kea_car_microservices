# External Library imports
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Trial stuff, delete later
from pydantic import BaseModel
from src.message_broker_management import TrialPublisher

class TrialMessage(BaseModel):
    message: str

load_dotenv()

app = FastAPI()

CORS_SETTINGS = {
    "allow_origins": ["*"],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"]
}

app.add_middleware(CORSMiddleware, **CORS_SETTINGS)

@app.get("/")
def read_root():
    return {"Hello": "Admin Service something EXTRA!!!"}

@app.get("/send_message/{message}")
def send_message(message: str):
    trial_publisher = TrialPublisher()
    trial_message = TrialMessage(message=message)
    trial_publisher.publish(trial_message)
    return {"message": "Message sent successfully"}



if __name__ == "__main__":
    import uvicorn
    
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    try:
        API_PORT = int(os.getenv("API_PORT", 8000))
    except ValueError:
        raise ValueError("API_PORT must be an integer.")
    
    uvicorn.run("main:app", host=API_HOST, port=API_PORT, reload=True)
