from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import logging
import asyncio
from rabbitmq.consumer import TrialConsumer

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

@asynccontextmanager
async def lifespan_of_consumer(app: FastAPI):
    """Lifespan function to handle startup and shutdown events."""
    # Startup logic
    
    try:
        logger.info("Starting RabbitMQ consumer...")
        consumer = TrialConsumer()
        app.state.consumer = consumer
        await consumer.connect()
        asyncio.create_task(consumer.start())
        logger.info("RabbitMQ consumer started successfully.")
    except ConnectionError as e:
        logger.error(f"Failed to start RabbitMQ consumer: {e}")
        raise e

    # Yield control to the application
    yield

    # Shutdown logic
    if app.state.consumer is not None and isinstance(app.state.consumer, TrialConsumer):
        logger.info("Stopping RabbitMQ consumer...")
        await app.state.consumer.stop()
        logger.info("RabbitMQ consumer stopped successfully.")
    else:
        logger.error("Consumer is not initialized or not of the correct type.")

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
    return {"message": "Auth Microservice is running!!!"}