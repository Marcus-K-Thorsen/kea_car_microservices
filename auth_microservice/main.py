from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
 
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
    return {"Hello": "Auth Service"}

if __name__ == "__main__":
    import uvicorn
    
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    try:
        API_PORT = int(os.getenv("API_PORT", 8001))
    except ValueError:
        raise ValueError("API_PORT must be an integer.")
    
    uvicorn.run("main:app", host=API_HOST, port=API_PORT, reload=True)