from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rabbitmq.rabbitmq_consume import Consumer
import threading

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

def consume_messages():
    consumer = Consumer(queue_name="messages")
    consumer.start()

if __name__ == "__main__":
    import uvicorn
    consume_thread = threading.Thread(target=consume_messages)
    consume_thread.start()
    uvicorn.run(app, host="127.0.0.1", port=8002)