from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from dotenv import load_dotenv
import os


app = FastAPI()

CORS_SETTINGS = {
    "allow_origins": ["*"],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"]
}

load_dotenv()

app.add_middleware(CORSMiddleware, **CORS_SETTINGS)

@app.get("/")
def read_root():
    return {"Hello": "Employee Service"}

if __name__ == "__main__":
    import uvicorn
    
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    try:
        API_PORT = int(os.getenv("API_PORT", 8003))
    except ValueError:
        raise ValueError("API_PORT must be an integer.")
    
    uvicorn.run("main:app", host=API_HOST, port=API_PORT, reload=True)
