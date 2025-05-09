from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.logger_tool import logger
import asyncio
import os
from dotenv import load_dotenv
from src.message_broker_management import get_admin_exchange_consumer, start_consumer, stop_consumer

load_dotenv()

@asynccontextmanager
async def lifespan_of_consumer(app: FastAPI):
    """Lifespan function to handle startup and shutdown events."""
    # Startup logic
    
    try:
        consumer = get_admin_exchange_consumer()
        app.state.consumer = consumer  # Store the consumer in the app state
        logger.info("Starting RabbitMQ consumer...")
        asyncio.create_task(start_consumer(consumer))
        logger.info("RabbitMQ consumer started successfully.")
    except Exception as e:
        logger.error(f"Failed to start RabbitMQ consumer: {e}")
        raise e

    # Yield control to the application
    yield
    
    consumer = app.state.consumer  # Retrieve the consumer from the app state
    # Shutdown logic
    if consumer:
        await stop_consumer(consumer)
    

app = FastAPI(
    lifespan=lifespan_of_consumer
)

CORS_SETTINGS = {
    "allow_origins": ["*"],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"]
}

app.add_middleware(CORSMiddleware, **CORS_SETTINGS)

@app.get("/")
def read_root():
    return {"message": "Auth Microservice is running!!"}

if __name__ == "__main__":
    import uvicorn
    
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    try:
        API_PORT = int(os.getenv("API_PORT", 8001))
    except ValueError:
        raise ValueError("API_PORT must be an integer.")
    
    uvicorn.run("main:app", host=API_HOST, port=API_PORT, reload=True)