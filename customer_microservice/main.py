"""
Main entry point for the Customer Microservice.

This module initializes the FastAPI application, configures middleware, and includes routers
that define the API endpoints for the microservice.

Key Responsibilities:
- Load environment variables from a `.env` file.
- Configure Cross-Origin Resource Sharing (CORS) settings.
- Include routers for various resources (e.g., models, brands, colors, etc.).
- Start the FastAPI application using Uvicorn when executed directly.

Note:
The actual endpoints are defined in the routers located in the `src.routers` package.
This file simply connects those routers to the FastAPI application.
"""

# External Library imports
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Internal library imports
from src.routers import (
    models_router,
    brands_router,
    colors_router,
    insurances_router,
    accessories_router
)
from scripts.seed_mongodb import seed_data_manually

# Initialize the FastAPI application
app = FastAPI()

# Configure CORS settings
CORS_SETTINGS = {
    "allow_origins": ["*"],  # Allow all origins
    "allow_credentials": True,
    "allow_methods": ["*"],  # Allow all HTTP methods
    "allow_headers": ["*"],  # Allow all headers
}

# Add CORS middleware to the application
app.add_middleware(CORSMiddleware, **CORS_SETTINGS)

# Include the Router endpoints in the main FastAPI app
# Each router corresponds to a specific resource (e.g., models, brands, etc.)
app.include_router(accessories_router, tags=["Accessories"])
app.include_router(brands_router, tags=["Brands"])
app.include_router(colors_router, tags=["Colors"])
app.include_router(insurances_router, tags=["Insurances"])
app.include_router(models_router, tags=["Models"])


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)


def start_application():
    """
    Start the Customer Microservice.

    This function runs the FastAPI application using Uvicorn as the ASGI server.
    The host and port are configurable via environment variables:
    - `API_HOST`: Host address (default: 0.0.0.0).
    - `API_PORT`: Port number (default: 8002).

    Example:
        poetry run python main.py
    """
    import uvicorn

    # Load API host and port from environment variables
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    try:
        API_PORT = int(os.getenv("API_PORT", 8002))
    except ValueError:
        raise ValueError("API_PORT must be an integer.")

    # Run the FastAPI application
    seed_data_manually()
    uvicorn.run("main:app", host=API_HOST, port=API_PORT, reload=True)


if __name__ == "__main__":
    start_application()
