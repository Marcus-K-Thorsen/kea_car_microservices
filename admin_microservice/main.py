# External Library imports
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from rabbitmq.publisher import Publisher

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
    to_employee_publisher = Publisher(exchange_name="admin_exchange", routing_key="employee.message")
    to_employee_publisher.publish(message)
    to_employee_publisher.close()
    to_auth_publisher = Publisher(exchange_name="admin_exchange", routing_key="auth.message")
    to_auth_publisher.publish(message)
    to_auth_publisher.close()
    return {"message": "Message sent successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
