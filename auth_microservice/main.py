# External Library imports
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import os
import sys
from dotenv import load_dotenv

# Internal Library imports
from src.message_broker_management import get_admin_exchange_consumer, start_consumer, stop_consumer
from src.logger_tool import logger
from src.routers import login_router

load_dotenv()

@asynccontextmanager
async def lifespan_of_consumer(app: FastAPI):
    """Lifespan function to handle startup and shutdown events."""
    # Startup logic
    
    try:
        consumer = get_admin_exchange_consumer()
        await consumer.connect()  # Connect to RabbitMQ
        app.state.consumer = consumer  # Store the consumer in the app state
        logger.info("Starting RabbitMQ consumer...")
        asyncio.create_task(start_consumer(consumer))
        logger.info("RabbitMQ consumer started successfully.")
    except Exception as e:
        logger.error(f"Failed to start RabbitMQ consumer: {e}")
        if app.state.consumer:
            await stop_consumer(app.state.consumer)  # Ensure consumer is stopped on failure
        os._exit(1)  # Exit the application if consumer fails to start
    logger.info("Authentication Microservice is starting up...")
    

    # Yield control to the application
    yield
    
    consumer = app.state.consumer  # Retrieve the consumer from the app state
    # Shutdown logic
    if consumer:
        await stop_consumer(consumer)
    

app = FastAPI(
    lifespan=lifespan_of_consumer,
    title="Authentication Microservice API",
    description="API for employee authentication in the KEA Cars system. Issues JWT tokens for secure access to protected endpoints. Synchronizes employee data with the admin microservice."
)

CORS_SETTINGS = {
    "allow_origins": ["*"],
    "allow_methods": ["*"],
    "allow_headers": ["*"]
}

app.add_middleware(CORSMiddleware, **CORS_SETTINGS)

# Include routers
app.include_router(
    login_router, tags=["Login"]
)



@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

if __name__ == "__main__":
    import uvicorn
    
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    try:
        API_PORT = int(os.getenv("API_PORT", 8001))
    except ValueError:
        raise ValueError("API_PORT must be an integer.")
    
    uvicorn.run("main:app", host=API_HOST, port=API_PORT, reload=True)
