# External Library imports
from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, Path, Query

# Internal library imports
from src.core import get_current_employee_token, TokenPayload
from src.database_management import Session, get_mysqldb
from src.services import purchases_service as service
from src.exceptions import handle_http_exception
from src.resources import (
    PurchaseReturnResource, 
    PurchaseCreateResource
)

router: APIRouter = APIRouter()

def get_db():
    with get_mysqldb() as session:
        yield session


@router.get(
    path="/purchases",
    response_model=List[PurchaseReturnResource],
    response_description=
    """
    Successfully retrieved a list of purchases.
    Returns: List[PurchaseReturnResource].
    """,
    summary="Retrieve Purchases - Requires authorization token in header.",
    description=
    """
    Retrieves all or a limited amount of Purchases and/or purchases belonging to a specifik employee 
    from the MySQL Employee database and returns a list of 'PurchaseReturnResource'.
    
    The endpoint requires an authorization token in the header and is accessible by all roles.
    But if the token is from an employee with the role: 'SALES_PERSON' then only purchases from that employee will be returned.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def get_purchases(
        employee_id: Optional[UUID] = Query(
            default=None,
            description=
            """
            The UUID of the employee,
            to retrieve purchases belonging to that employee.
            """
        ),
        limit: Optional[int] = Query(
            default=None, ge=1,
            description="""Set a limit for the amount of purchases that is returned."""
        ),
        session: Session = Depends(get_db),
        token: TokenPayload = Depends(get_current_employee_token)
):
    return await handle_http_exception(
        error_message="Failed to get purchases from the MySQL Employee database",
        callback=lambda: service.get_all(
            session,
            token,
            employee_id=None if not employee_id else str(employee_id),
            purchase_limit=limit
        )
    )


@router.get(
    path="/purchases/{purchase_id}",
    response_model=PurchaseReturnResource,
    response_description=
    """
    Successfully retrieved a purchase.
    Returns: PurchaseReturnResource.
    """,
    summary="Retrieve a Purchase by ID - Requires authorization token in header.",
    description=
    """
    Retrieves a Purchase by ID from the MySQL Employee database 
    by giving a UUID in the path for the purchase and 
    returns it as a 'PurchaseReturnResource'.
    
    The endpoint requires an authorization token in the header and is accessible by all roles.
    But if the token is from an employee with the role: 'SALES_PERSON' then only that employee's purchase can be retrieved.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def get_purchase(
        purchase_id: UUID = Path(
            default=...,
            description="""The UUID of the purchase to retrieve."""
        ),
        session: Session = Depends(get_db),
        token: TokenPayload = Depends(get_current_employee_token)
):
    return await handle_http_exception(
        error_message="Failed to get purchase from the MySQL Employee database",
        callback=lambda: service.get_by_id(
            session,
            token,
            purchase_id=str(purchase_id)
        )
    )


@router.get(
    path="/purchases/car/{cars_id}",
    response_model=PurchaseReturnResource,
    response_description=
    """
    Successfully retrieved a purchase.
    Returns: PurchaseReturnResource.
    """,
    summary="Retrieve a Purchase by Car ID - Requires authorization token in header.",
    description=
    """
    Retrieves a Purchase by Car ID from the MySQL database 
    by giving a UUID in the path for the car of the purchase 
    and returns it as a 'PurchaseReturnResource'.
    
    The endpoint requires an authorization token in the header and is accessible by all roles.
    But if the token is from an employee with the role: 'SALES_PERSON' and the car is not of that employee, 
    than an error with status code HTTP_403_FORBIDDEN will be thrown.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def get_purchase_by_car_id(
        cars_id: UUID = Path(
            default=...,
            description="""The UUID of the purchase's car to retrieve."""
        ),
        session: Session = Depends(get_db),
        token: TokenPayload = Depends(get_current_employee_token)
):
    return await handle_http_exception(
        error_message="Failed to get purchase by car id from the MySQL Employee database",
        callback=lambda: service.get_by_car_id(
            session,
            token,
            car_id=str(cars_id)
        )
    )


@router.post(
    path="/purchases",
    response_model=PurchaseReturnResource,
    response_description=
    """
    Successfully created a purchase.
    Returns: PurchaseReturnResource.
    """,
    summary="Create a Purchase - Requires authorization token in header.",
    description=
    """
    Creates a Purchase within the MySQL Employee database 
    by giving a request body 'PurchaseCreateResource' 
    and returns it as a 'PurchaseReturnResource'.
    
    The endpoint requires an authorization token in the header and is accessible by all roles.
    But if the token is from an employee with the role: 'SALES_PERSON' and car being purchased is not of that employee,
    than an error with status code HTTP_403_FORBIDDEN will be thrown.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def create_purchase(
        purchase_create_data: PurchaseCreateResource,
        session: Session = Depends(get_db),
        token: TokenPayload = Depends(get_current_employee_token)
):
    return await handle_http_exception(
        error_message="Failed to create purchase within the MySQL Employee database",
        callback=lambda: service.create(
            session,
            token,
            purchase_create_data
        )
    )
