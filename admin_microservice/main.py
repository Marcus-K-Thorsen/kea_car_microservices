# External Library imports
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from .rabbitmq.publisher import MessagePublisher as Publisher

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
    return {"Hello": "World"}

@app.get("/send_message/{message}")
def send_message(message: str):
    message_publisher = Publisher()
    message_publisher.publish(message)
    message_publisher.close_connection()
    return {"message": "Message sent successfully"}

# To run the microservice, run this script while in the root of the project directory:
# poetry run python -m admin_microservice.main
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
