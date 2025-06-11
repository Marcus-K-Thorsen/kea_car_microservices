# External Libary imports
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.responses import Response
from dotenv import load_dotenv
from fastapi import FastAPI
import asyncio
import os

# Internal Library imports
from src.message_broker_management import get_admin_exchange_consumer, start_consumer, stop_consumer
from src.routers import (
    accessories_router,
    insurances_router,
    employees_router,
    customers_router,
    purchases_router,
    colors_router,
    brands_router,
    models_router,
    login_router,
    cars_router
)
from src.logger_tool import logger


@asynccontextmanager
async def lifespan_of_consumer(app: FastAPI):
    """Lifespan function to handle startup and shutdown events."""
    # Startup logic
    try:
        consumer = get_admin_exchange_consumer()
        await consumer.connect()
        app.state.consumer = consumer  # Store the consumer in the app state
        logger.info("Starting RabbitMQ consumer...")
        asyncio.create_task(start_consumer(consumer))
        logger.info("RabbitMQ consumer started successfully.")
    except Exception as e:
        logger.error(f"Failed to start RabbitMQ consumer: {e}")
        if app.state.consumer:
            await stop_consumer(app.state.consumer)
        os._exit(1)  # Exit the application if consumer fails to start
    logger.info("Employee Microservice is starting up...")

    # Yield control to the application
    yield
    
    consumer = app.state.consumer  # Retrieve the consumer from the app state
    # Shutdown logic
    if consumer:
        await stop_consumer(consumer)



app = FastAPI(
    lifespan=lifespan_of_consumer,
    title="Employee Microservice API",
    description="API for managing brands, models, colors, accessories, insurances, customers, cars, and purchases in the KEA Cars system. Used by employees (admins, managers, sales people). Handles business logic, enforces role-based access, and synchronizes employee data with the admin microservice."
)


CORS_SETTINGS = {
    "allow_origins": ["*"],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"]
}

load_dotenv()

app.add_middleware(CORSMiddleware, **CORS_SETTINGS)


app.include_router(accessories_router, tags=["Accessories"])
app.include_router(brands_router, tags=["Brands"])
app.include_router(cars_router, tags=["Cars"])
app.include_router(colors_router, tags=["Colors"])
app.include_router(customers_router, tags=["Customers"])
app.include_router(employees_router, tags=["Employees"])
app.include_router(insurances_router, tags=["Insurances"])
app.include_router(models_router, tags=["Models"])
app.include_router(purchases_router, tags=["Purchases"])
app.include_router(login_router, tags=["Login"])


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)


if __name__ == "__main__":
    import uvicorn
    
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    try:
        API_PORT = int(os.getenv("API_PORT", 8003))
    except ValueError:
        raise ValueError("API_PORT must be an integer.")
    
    uvicorn.run("main:app", host=API_HOST, port=API_PORT, reload=True)
    