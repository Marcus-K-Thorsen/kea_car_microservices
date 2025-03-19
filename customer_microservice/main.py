from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

 
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

# To run the customer microservice endpoints, run this script while in the root of the project directory:
# poetry run python -m customer_microservice.main
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)