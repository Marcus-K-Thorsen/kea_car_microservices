# External Library imports
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from .rabbitmq.publisher import MessagePublisher as Publisher

class TrialItem(BaseModel):
    item_name: str

class Trial(BaseModel):
    name: str
    age: int
    trial_item: TrialItem

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
    return {"Hello": "Employee Service"}

@app.get("/send_message/{message}")
def send_message(message: str):
    trial_item = TrialItem(item_name=message)
    trial = Trial(name="employee", age=20, trial_item=trial_item)
    
    message_publisher = Publisher()
    message_publisher.publish(trial)
    message_publisher.close_connection()
    return {"message": "Message sent successfully"}

# To run the employee microservice endpoints, run this script while in the root of the project directory:
# poetry run python -m employee_microservice.main
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8003)
