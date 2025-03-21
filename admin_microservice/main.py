# External Library imports
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from main_publisher import main as send_trial_message

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
    return {"Hello": "Admin Service something EXTRA"}

@app.get("/send_message/{message}")
def send_message(message: str):
    send_trial_message(message)
    return {"message": "Message sent successfully"}


