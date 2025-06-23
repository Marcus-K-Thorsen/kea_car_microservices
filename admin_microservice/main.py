# External Library imports
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Internal library imports
from src.routers import employees_router, login_router


load_dotenv()

app = FastAPI(
    title="Admin Microservice API",
    description="API for managing employee records in the KEA Cars system. Only accessible to admin users. Supports creation, retrieval, update, deletion, and undeletion of employee accounts."
)

CORS_SETTINGS = {
    "allow_origins": ["*"],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}


app.add_middleware(CORSMiddleware, **CORS_SETTINGS)

app.include_router(employees_router, tags=["Employees"])
app.include_router(login_router, tags=["Login"])


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)


if __name__ == "__main__":
    import uvicorn

    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    try:
        API_PORT = int(os.getenv("API_PORT", 8000))
    except ValueError:
        raise ValueError("API_PORT must be an integer.")

    uvicorn.run("main:app", host=API_HOST, port=API_PORT, reload=True)
