# External Library imports
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from main_publisher import main as send_trial_message

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
    return {"Hello": "Admin Service"}

@app.get("/send_message/{message}")
def send_message(message: str):
    send_trial_message(message)
    return {"message": "Message sent successfully"}

# To run the admin microservice endpoints, run this script while in the root of the project directory:
# poetry run python -m admin_microservice.main
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
