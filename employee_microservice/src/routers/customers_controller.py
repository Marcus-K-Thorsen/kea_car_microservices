# External Library imports
from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, Path, Query, Body, status

# Internal library imports
from src.core import get_current_employee_token, TokenPayload
from src.database_management import Session, get_mysqldb
from src.services import customers_service as service
from src.exceptions import handle_http_exception
from src.resources import (
    CustomerReturnResource, 
    CustomerCreateResource, 
    CustomerUpdateResource
)

router: APIRouter = APIRouter()

def get_db():
    with get_mysqldb() as session:
        yield session



@router.get(
    path="/customers",
    response_model=List[CustomerReturnResource],
    response_description=
    """
    Successfully retrieved a list of customers. 
    Returns: List[CustomerReturnResource].
    """,
    summary="Retrieve Customers - Requires authorization token in header.",
    description=
    """
    Retrieves all or a limited amount of Customers from 
    the MySQL Employee database potentially filtered by email 
    and returns a list of 'CustomerReturnResource'.
    
    The endpoint requires an authorization token in the header and is accessible by all roles.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def get_customers(
        email_filter: Optional[str] = Query(
            default=None, min_length=1,
            description="""Filter customers by their email."""
        ),
        limit: Optional[int] = Query(
            default=None, ge=1,
            description="""Set a limit for the amount of customers that is returned."""
        ),
        session: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_employee_token)
):
    return await handle_http_exception(
        error_message="Failed to get customers from the MySQL Employee database",
        callback=lambda: service.get_all(
            session,
            token_payload,
            filter_customer_by_email=email_filter,
            customer_limit=limit
        )
    )


@router.get(
    path="/customers/{customer_id}",
    response_model=CustomerReturnResource,
    response_description=
    """
    Successfully retrieved a customer.
    Returns: CustomerReturnResource.
    """,
    summary="Retrieve a Customer by ID - Requires authorization token in header.",
    description=
    """
    Retrieves a Customer by ID from the MySQL Employee database 
    and returns it as a 'CustomerReturnResource'.
    
    The endpoint requires an authorization token in the header and is accessible by all roles.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def get_customer(
        customer_id: UUID = Path(
            default=...,
            description="""The UUID of the customer to retrieve."""
        ),
        session: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_employee_token)
):
    return await handle_http_exception(
        error_message="Failed to get customer from the MySQL Employee database",
        callback=lambda: service.get_by_id(
            session,
            token_payload,
            customer_id=str(customer_id)
        )
    )


@router.post(
    path="/customers",
    response_model=CustomerReturnResource,
    response_description=
    """
    Successfully created a customer.
    Returns: CustomerReturnResource.
    """,
    summary="Create a Customer - Requires authorization token in header.",
    description=
    """
    Creates a Customer within the MySQL Employee database 
    by giving a request body 'CustomerCreateResource' 
    and returns it as a 'CustomerReturnResource'.
    
    The endpoint requires an authorization token in the header and is accessible by all roles.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def create_customer(
        customer_create_data: CustomerCreateResource,
        session: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_employee_token)
):
    return await handle_http_exception(
        error_message="Failed to create customer within the MySQL Employee database",
        callback=lambda: service.create(
            session,
            token_payload,
            customer_create_data
        )
    )


@router.put(
    path="/customers/{customer_id}",
    response_model=CustomerReturnResource,
    response_description=
    """
    Successfully updated a customer.
    Returns: CustomerReturnResource.
    """,
    summary="Update a Customer - Requires authorization token in header.",
    description=
    """
    Updates a Customer within the MySQL Employee database 
    by giving a UUID in the path for the customer 
    and by giving a request body 'CustomerUpdateResource' 
    and returns it as a 'CustomerReturnResource'.
    
    The endpoint requires an authorization token in the header and is accessible by all roles.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def update_customer(
        customer_id: UUID = Path(
            default=...,
            description="""The UUID of the customer to update."""
        ),
        customer_update_data: CustomerUpdateResource = Body(
            default=...,
            title="CustomerUpdateResource"
        ),
        session: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_employee_token)
):
    return await handle_http_exception(
        error_message="Failed to update customer within the MySQL Employee database",
        callback=lambda: service.update(
            session,
            token_payload,
            customer_id=str(customer_id),
            customer_update_data=customer_update_data
        )
    )


@router.delete(
    path="/customers/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description=
    """
    Successfully deleted a customer.
    Returns: 204 No Content.
    """,
    summary="Delete a Customer - Requires authorization token in header.",
    description=
    """
    Deletes a Customer within the MySQL Employee database 
    by giving a UUID in the path for the customer 
    and returns a 204 status code.
    
    The endpoint requires an authorization token in the header and is only accessible by employees with the role: 'ADMIN' or 'MANAGER'.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def delete_customer(
        customer_id: UUID = Path(
            default=...,
            description="""The UUID of the customer to delete."""
        ),
        session: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_employee_token)
):
    return await handle_http_exception(
        error_message="Failed to delete customer within the MySQL Employee database",
        callback=lambda: service.delete(
            session,
            token_payload,
            customer_id=str(customer_id)
        )
    )
