# External Library imports
from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, Path, Query

# Internal library imports
from src.exceptions import handle_http_exception
from src.logger_tool import logger
from src.core import get_current_employee_token, TokenPayload
from src.services import employees_service as service
from src.database_management import Session, get_mysqldb
from src.resources import (
    EmployeeReturnResource
)


router: APIRouter = APIRouter()


def get_db():
    with get_mysqldb() as session:
        yield session
        
@router.get(
    path="/employees",
    response_model=List[EmployeeReturnResource],
    response_description=
    """
    Successfully retrieved a list of employees.
    Returns: List[EmployeeReturnResource].
    """,
    summary="Retrieve Employees - Requires authorization token in header.",
    description=
    """
        Retrieves a list of employees from the MySQL Employee database based on the provided query parameters.

        - If no query parameters are provided, the endpoint returns all active employees.
        - The `limit` query parameter can be used to restrict the number of employees returned.
        - The `deleted` query parameter allows filtering employees based on their deletion status:
            - `None` (default): Returns only active employees.
            - `True`: Returns only deleted employees.
            - `False`: Returns both active and deleted employees.

        The response is a list of employees represented as 'EmployeeReturnResource' objects.
        The endpoint requires an authorization token in the header and is accessible by all roles.
        But if the token is from an employee with the role: 'SALES_PERSON' then a list with only that employee will be returned.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def get_employees(
        limit: Optional[int] = Query(
            default=None, ge=1,
            description="""Set a limit for the amount of employees that is returned."""
        ),
        deleted: Optional[bool] = Query(
            default=None,
            description="""Set a filter for deleted employees.
                            - `None` (default behavior): Only active employees.
                            - `True`: Only deleted employees.
                            - `False`: Both active and deleted employees."""
        ),
        session: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_employee_token)
):
    return handle_http_exception(
        error_message="Failed to get employees from the MySQL Employee database",
        callback=lambda: service.get_all(
            session,
            token_payload,
            employee_limit=limit,
            is_deleted_filter=deleted
        )
    )


@router.get(
    path="/employees/{employee_id}",
    response_model=EmployeeReturnResource,
    response_description=
    """
    Successfully retrieved an employee.
    Returns: EmployeeReturnResource.
    """,
    summary="Retrieve an Employee by ID - Requires authorization token in header.",
    description=
    """
    Retrieves an Employee by ID from the MySQL Employee database 
    by giving a UUID in the path for the employee 
    and returns it as a 'EmployeeReturnResource'.
    
    The endpoint requires an authorization token in the header and is accessible by all roles.
    But if the token is from an employee with the role: 'SALES_PERSON' then that employee will be returned.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def get_employee(
        employee_id: UUID = Path(
            default=...,
            description="""The UUID of the employee to retrieve."""
        ),
        session: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_employee_token)
):
    logger.info(f"Token Id: {token_payload.employee_id}")
    return handle_http_exception(
        error_message="Failed to get employee from the MySQL Employee database",
        callback=lambda: service.get_by_id(
            session,
            token_payload,
            employee_id=str(employee_id)
        )
    )
