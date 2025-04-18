from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import asyncio
import uvicorn
from rabbitmq.consumer import TrialConsumer

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
    return {"message": "Auth Microservice is running!!!"}

# Create an instance of TrialConsumer
trial_consumer = TrialConsumer()

@app.on_event("startup")
async def on_startup():
    """Start the RabbitMQ consumer on application startup."""
    await trial_consumer.connect()
    asyncio.create_task(trial_consumer.start())

@app.on_event("shutdown")
async def on_shutdown():
    """Stop the RabbitMQ consumer on application shutdown."""
    await trial_consumer.stop()

if __name__ == "__main__":
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    try:
        API_PORT = int(os.getenv("API_PORT", 8001))
    except ValueError:
        raise ValueError("API_PORT must be an integer.")

    # Start the FastAPI application
    uvicorn.run("main:app", host=API_HOST, port=API_PORT, reload=True)