# External Library imports
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

# Internal library imports
from src.routers import (
    models_router,
    brands_router,
    colors_router,
    insurances_router,
    accessories_router
)

 
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
    return {"Hello": "Customer Service"}

# Including the Router endpoints in the main FastAPI app
app.include_router(accessories_router, prefix="/api", tags=["Accessories"])
app.include_router(brands_router, prefix="/api", tags=["Brands"])
app.include_router(colors_router, prefix="/api", tags=["Colors"])
app.include_router(insurances_router, prefix="/api", tags=["Insurances"])
app.include_router(models_router, prefix="/api", tags=["Models"])


if __name__ == "__main__":
    import uvicorn
    
    API_HOST = os.getenv("API_HOST", "127.0.0.1")
    try:
        API_PORT = int(os.getenv("API_PORT", 8002))
    except ValueError:
        raise ValueError("API_PORT must be an integer.")
    
    uvicorn.run(app, host=API_HOST, port=API_PORT)
