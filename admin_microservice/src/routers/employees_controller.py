# External Library imports
from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, Path, Query, Body

# Internal library imports
from src.exceptions import handle_http_exception
from src.services import employees_service as service
from src.database_management import Session, get_mysqldb
from src.resources import (
    EmployeeCreateResource, 
    EmployeeUpdateResource, 
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
        Retrieves a list of employees from the MySQL Admin database based on the provided query parameters.

        - If no query parameters are provided, the endpoint returns all active employees.
        - The `limit` query parameter can be used to restrict the number of employees returned.
        - The `deleted` query parameter allows filtering employees based on their deletion status:
            - `None` (default): Returns only active employees.
            - `True`: Returns only deleted employees.
            - `False`: Returns both active and deleted employees.

        The response is a list of employees represented as 'EmployeeReturnResource' objects.
    """,
    #dependencies=[Depends(get_current_employee_token)]
)
async def get_emplyees(
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
        session: Session = Depends(get_db)
):
    return handle_http_exception(
        error_message="Failed to get employees from the MySQL Admin database",
        callback=lambda: service.get_all(
            session,
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
    Retrieves an Employee by ID from the MySQL Admin database 
    by giving a UUID in the path for the employee 
    and returns it as a 'EmployeeReturnResource'.
    """,
    #dependencies=[Depends(get_current_employee_token)]
)
async def get_employee(
        employee_id: UUID = Path(
            default=...,
            description="""The UUID of the employee to retrieve."""
        ),
        session: Session = Depends(get_db)
):
    return handle_http_exception(
        error_message="Failed to get employee from the MySQL Admin database",
        callback=lambda: service.get_by_id(
            session,
            employee_id=str(employee_id)
        )
    )


@router.post(
    path="/employees",
    response_model=EmployeeReturnResource,
    response_description=
    """
    Successfully created an employee.
    Returns: EmployeeReturnResource.
    """,
    summary="Create an Employee - Requires authorization token in header.",
    description=
    """
    Creates an Employee within the MySQL Admin database 
    by giving a request body 'EmployeeCreateResource' 
    and returns it as a 'EmployeeReturnResource'.
    """,
    #dependencies=[Depends(get_current_employee_token)]
)
async def create_employee(
        employee_create_data: EmployeeCreateResource,
        session: Session = Depends(get_db)
):
    return handle_http_exception(
        error_message="Failed to create employee within the MySQL Admin database",
        callback=lambda: service.create(
            session,
            employee_create_data
        )
    )

@router.put(
    path="/employees/{employee_id}",
    response_model=EmployeeReturnResource,
    response_description=
    """
    Successfully updated an employee.
    Returns: EmployeeReturnResource.
    """,
    summary="Update an Employee - Requires authorization token in header.",
    description=
    """
    Updates an Employee within the MySQL Admin database 
    by giving a UUID in the path for the employee 
    and a request body 'EmployeeUpdateResource' 
    and returns it as a 'EmployeeReturnResource'.
    """,
    #dependencies=[Depends(get_current_employee_token)]
)
async def update_employee(
        employee_id: UUID = Path(
            default=...,
            description="""The UUID of the employee to update."""
        ),
        employee_update_data: EmployeeUpdateResource = Body(
            default=...,
            title="EmployeeUpdateResource"
        ),
        session: Session = Depends(get_db)
):
    return handle_http_exception(
        error_message="Failed to update employee within the MySQL Admin database",
        callback=lambda: service.update(
            session,
            employee_id=str(employee_id),
            employee_update_data=employee_update_data
        )
    )

@router.delete(
    path="/employees/{employee_id}",
    response_model=EmployeeReturnResource,
    response_description=
    """
    Successfully deleted an employee.
    Returns: EmployeeReturnResource.
    """,
    summary="Delete an Employee - Requires authorization token in header.",
    description=
    """
    Deletes an Employee within the MySQL Admin database 
    by giving a UUID in the path for the employee 
    and returns it as a 'EmployeeReturnResource'.
    """,
    #dependencies=[Depends(get_current_employee_token)]
)
async def delete_employee(
        employee_id: UUID = Path(
            default=...,
            description="""The UUID of the employee to delete."""
        ),
        session: Session = Depends(get_db)
):
    return handle_http_exception(
        error_message="Failed to delete employee within the MySQL Admin database",
        callback=lambda: service.delete(
            session,
            employee_id=str(employee_id)
        )
    )
    
@router.patch(
    path="/employees/{employee_id}/undelete",
    response_model=EmployeeReturnResource,
    response_description="""
    Successfully undeleted an employee.
    Returns: EmployeeReturnResource.
    """,
    summary="Undelete an Employee - Requires authorization token in header.",
    description="""
    Undeletes an Employee within the MySQL Admin database 
    by giving a UUID in the path for the employee 
    and returns it as a 'EmployeeReturnResource'.
    """,
    #dependencies=[Depends(get_current_employee_token)]
)
async def undelete_employee(
        employee_id: UUID = Path(
            default=...,
            description="""The UUID of the employee to undelete."""
        ),
        session: Session = Depends(get_db)
):
    return handle_http_exception(
        error_message="Failed to undelete employee within the MySQL Admin database",
        callback=lambda: service.undelete(
            session,
            employee_id=str(employee_id)
        )
    )