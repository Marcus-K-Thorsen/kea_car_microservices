# External Library imports
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from rabbitmq.consumer import Consumer

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
    return {"Hello customer": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
