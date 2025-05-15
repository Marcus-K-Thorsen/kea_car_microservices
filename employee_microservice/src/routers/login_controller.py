# External Library imports
from fastapi import APIRouter, Form, HTTPException
import requests

# Internal library imports
from src.core import Token
from src.resources import EmployeeLoginResource


router: APIRouter = APIRouter()


@router.post(
    path="/token",
    response_model=Token,
    response_description=
    """
    Successfully created a token.
    Returns: Token.
    """,
    summary="Create an Access Token for an Employee.",
    description=
    """
    This endpoint is needed for the Swagger UI 
    can authorize access to endpoints 
    that needs authorization. Creates an Access Token 
    from an employee within the MongoDB database by 
    giving Forms for the email and password of that employee
    and returns a 'Token' from the Auth Microservice '/token' endpoint.
    """
)
async def login_for_access_token(
        username: str = Form(
            default=...,
            description="""The email of the employee."""
        ),
        password: str = Form(
            default=...,
            description="""The password of the employee."""
        )
):
    
    employee_login_data = EmployeeLoginResource(
        email=username,
        password=password
    )
    
    # Send a POST request to the Auth Microservice
    auth_microservice_url = "http://auth_microservice:8001/login"
    response = requests.post(
        auth_microservice_url,
        json=employee_login_data.model_dump(),
        headers={"Content-Type": "application/json"}
    )
    
    # Check if the request was successful
    if response.status_code == 200:
        return Token(**response.json())
    else:
        # Handle the error response from the Auth Microservice
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json().get("detail", "Failed to create an access token.")
        )



