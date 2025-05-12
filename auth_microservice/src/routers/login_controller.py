# External Library imports
from fastapi import APIRouter, Depends, Form

# Internal library imports
from src.database_management import Database, get_mongodb
from src.exceptions.error_handler import handle_http_exception
from src.services import login_service as service
from src.core import Token
from src.resources import EmployeeLoginResource


router: APIRouter = APIRouter()


def get_db():
    with get_mongodb() as database:
        yield database


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
    giving Forms for the email and password of that 
    employee and returns a 'Token'.
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
        ),
        database: Database = Depends(get_db)
):  # pragma: no cover
    return handle_http_exception(
        error_message="Failed to create an access token for an Employee in the MongoDB Auth database",
        callback=lambda: service.login(
            database,
            employee_login_data=EmployeeLoginResource(
                email=username,
                password=password
            )
        )
    )


@router.post(
    path="/login",
    response_model=Token,
    response_description=
    """
    Successfully logged in.
    Returns: Token.
    """,
    summary="Logs in as an Employee.",
    description=
    """
    Works the same as the '/token' endpoint, 
    but requires a request body instead of forms, 
    this endpoint is to make it easier for the frontend 
    to log in and access endpoints that needs authorization. 
    Logs in as a employee within the MongoDB database by 
    giving a request body 'EmployeeLoginResource' 
    of that employee and returns a 'Token'.
    """
)
async def login(
        employee_login_data: EmployeeLoginResource,
        database: Database = Depends(get_db)
):  # pragma: no cover
    return handle_http_exception(
        error_message="Failed to login for a Employee in the MongoDB Auth database",
        callback=lambda: service.login(
            database,
            employee_login_data
        )
    )


