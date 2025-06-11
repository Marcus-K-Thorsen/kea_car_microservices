# External Library imports
from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, Path, Query, status

# Internal library imports
from src.core import get_current_employee_token, TokenPayload
from src.database_management import Session, get_mysqldb
from src.services import cars_service as service
from src.exceptions import handle_http_exception
from src.resources import (
    CarReturnResource, 
    CarCreateResource
)

router: APIRouter = APIRouter()

def get_db():
    with get_mysqldb() as session:
        yield session


@router.get(
    path="/cars",
    response_model=List[CarReturnResource],
    response_description=
    """
    Successfully retrieved list a of cars. 
    Returns: List[CarReturnResource].
    """,
    summary="Retrieve Cars - Requires authorization token in header.",
    description=
    """
    Retrieves all or a limited amount of Cars from the MySQL Employee database,
    potentially filtered by cars belonging to a customer and/or employee, 
    if the cars are purchased and/or is past their purchase deadline,
    and returns a list of 'CarReturnResource'.
    
    The endpoint requires an authorization token in the header and is accessible by all roles.
    But if the token is from an employee with the role: 'SALES_PERSON' then only cars from that employee will be returned.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def get_cars(
        customer_id: Optional[UUID] = Query(
            default=None,
            description=
            """
            The UUID of the customer, 
            to retrieve cars belonging to that customer.
            """
        ),
        employee_id: Optional[UUID] = Query(
            default=None,
            description=
            """
            The UUID of the employee, 
            to retrieve cars belonging to that employee.
            """
        ),
        is_purchased: Optional[bool] = Query(
            default=None,
            description=
            """
            Set to: 
            'true' to retrieve only purchased cars, 
            'false' to retrieve only cars that has not been purchased 
            and default retrieves both purchased and non-purchased cars.
            """
        ),
        is_past_purchase_deadline: Optional[bool] = Query(
            default=None,
            description=
            """
            Set to: 
            'true' to retrieve only cars past purchase deadline, 
            'false' to retrieve only cars that has not past the purchased deadline 
            and default retrieves cars that is past and not past purchase deadline.
            """
        ),
        limit: Optional[int] = Query(
            default=None, ge=1,
            description="""Set a limit for the amount of cars that is returned."""
        ),
        session: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_employee_token)
):
    return handle_http_exception(
        error_message="Failed to get cars from the MySQL Employee database",
        callback=lambda: service.get_all(
            session,
            token_payload,
            customer_id=None if not customer_id else str(customer_id),
            employee_id=None if not employee_id else str(employee_id),
            is_purchased=is_purchased,
            is_past_purchase_deadline=is_past_purchase_deadline,
            car_limit=limit
        )
    )


@router.get(
    path="/cars/{car_id}",
    response_model=CarReturnResource,
    response_description=
    """
    Successfully retrieved a car. 
    Returns: CarReturnResource
    """,
    summary="Retrieve a Car by ID - Requires authorization token in header.",
    description=
    """
    Retrieves a Car by ID from the MySQL Employee database by giving a UUID 
    in the path for the car and returns it as a 'CarReturnResource'.
    
    The endpoint requires an authorization token in the header and is accessible by all roles.
    But if the token is from an employee with the role: 'SALES_PERSON' then only that employee's car can be retrieved.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def get_car(
        car_id: UUID = Path(
            default=...,
            description="""The UUID of the car to retrieve."""
        ),
        session: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_employee_token)
):
    return handle_http_exception(
        error_message="Failed to get car from the MySQL Employee database",
        callback=lambda: service.get_by_id(
            session,
            token_payload,
            car_id=str(car_id)
        )
    )


@router.post(
    path="/cars",
    response_model=CarReturnResource,
    response_description=
    """
    Successfully created a car. 
    Returns: CarReturnResource.
    """,
    summary="Create a Car - Requires authorization token in header.",
    description=
    """
    Creates a Car within the MySQL Employee database 
    by giving a request body 'CarCreateResource' 
    and returns it as a 'CarReturnResource'.
    
    The endpoint requires an authorization token in the header and is accessible by all roles.
    But if the token is from an employee with the role: 'SALES_PERSON' then that employee will be set as the owner.
    Or if no employee is given in the request body then the employee that created the car will be set as the owner.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def create_car(
        car_create_data: CarCreateResource,
        session: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_employee_token)
):
    return handle_http_exception(
        error_message="Failed to create car within the MySQL Employee database",
        callback=lambda: service.create(
            session,
            token_payload,
            car_create_data
        )
    )


@router.delete(
    path="/cars/{car_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description=
    """
    Successfully deleted a car.
    Returns: 204 No Content.
    """,
    summary="Delete a Car - Requires authorization token in header.",
    description=
    """
    Deletes a Car within the MySQL Employee database 
    by giving a UUID in the path for the car 
    and returns a 204 status code.
    
    The endpoint requires an authorization token in the header and is accessible by all roles.
    But if the token is from an employee with the role: 'SALES_PERSON' and the car is not of that employee, 
    than an error with status code HTTP_403_FORBIDDEN will be thrown.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def delete_car(
        car_id: UUID = Path(
            default=...,
            description="""The UUID of the car to delete."""
        ),
        delete_purchase_too: bool = Query(
            default=False,
            description=
            """
            A boolean that is default False, 
            for if you are certain you want to delete 
            the car with its purchase if it has one.
            """
        ),
        session: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_employee_token)
):
    return handle_http_exception(
        error_message="Failed to delete car within the MySQL Employee database",
        callback=lambda: service.delete(
            session,
            token_payload,
            car_id=str(car_id),
            delete_purchase_too=delete_purchase_too
        )
    )
