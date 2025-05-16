# External Library imports
from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, Path, Query, Body

# Internal library imports
from src.core import get_current_employee_token, TokenPayload
from src.database_management import Session, get_mysqldb
from src.services import insurances_service as service
from src.exceptions import handle_http_exception
from src.resources import (
    InsuranceReturnResource,
    InsuranceCreateResource,
    InsuranceUpdateResource
)


router: APIRouter = APIRouter()

def get_db():
    with get_mysqldb() as session:
        yield session


@router.get(
    path="/insurances",
    response_model=List[InsuranceReturnResource],
    response_description=
    """
    Successfully retrieved a list of insurances.
    Returns: List[InsuranceReturnResource].
    """,
    summary="Retrieve Insurances - Requires authorization token in header.",
    description=
    """
    Retrieves all or a limited amount of Insurances from the 
    MySQL Employee database and returns a list of 'InsuranceReturnResource'.
    
    The endpoint requires an authorization token in the header and is accessible by all roles.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def get_insurances(
        limit: Optional[int] = Query(
            default=None, ge=1,
            description="""Set a limit for the amount of insurances that is returned."""
        ),
        session: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_employee_token)
):
    return handle_http_exception(
        error_message="Failed to get insurances from the MySQL Employee database",
        callback=lambda: service.get_all(
            session,
            token_payload,
            insurance_limit=limit
        )
    )

@router.get(
    path="/insurances/{insurance_id}",
    response_model=InsuranceReturnResource,
    response_description=
    """
    Successfully retrieved an insurance.
    Returns: InsuranceReturnResource.
    """,
    summary="Retrieve an Insurance by ID - Requires authorization token in header.",
    description=
    """
    Retrieves an Insurance by ID from the MySQL Employee database 
    by giving a UUID in the path for the insurance 
    and returns it as an 'InsuranceReturnResource'.
    
    The endpoint requires an authorization token in the header and is accessible by all roles.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def get_insurance(
        insurance_id: UUID = Path(
            default=...,
            description="""The UUID of the insurance to retrieve."""
        ),
        session: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_employee_token)
):
    return handle_http_exception(
        error_message="Failed to get insurance from the MySQL Employee database",
        callback=lambda: service.get_by_id(
            session,
            token_payload,
            insurance_id=str(insurance_id)
        )
    )
    

@router.post(
    path="/insurances",
    response_model=InsuranceReturnResource,
    response_description=
    """
    Successfully created an insurance.
    Returns: InsuranceReturnResource.
    """,
    summary="Create an Insurance - Requires authorization token in header.",
    description=
    """
    Creates an Insurance in the MySQL Employee database 
    and returns it as an 'InsuranceReturnResource'.
    
    If successful a message will be send to the 'synch_microservice', 
    to create that insurance in the Customer database as well.
    
    The endpoint requires an authorization token in the header and is only accessible by employees with the role: 'ADMIN' or 'MANAGER'.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def create_insurance(
        insurance_create_data: InsuranceCreateResource,
        session: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_employee_token)
):
    return handle_http_exception(
        error_message="Failed to create insurance in the MySQL Employee database",
        callback=lambda: service.create(
            session,
            token_payload,
            insurance_create_data
        )
    )


@router.put(
    path="/insurances/{insurance_id}",
    response_model=InsuranceReturnResource,
    response_description=
    """
    Successfully updated an insurance.
    Returns: InsuranceReturnResource.
    """,
    summary="Update an Insurance - Requires authorization token in header.",
    description=
    """
    Updates an Insurance in the MySQL Employee database 
    and returns it as an 'InsuranceReturnResource'.
    
    If successful a message will be send to the 'synch_microservice', 
    to update that insurance in the Customer database as well.
    
    The endpoint requires an authorization token in the header and is only accessible by employees with the role: 'ADMIN' or 'MANAGER'.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def update_insurance(
        insurance_id: UUID = Path(
            default=...,
            description="""The UUID of the insurance to update."""
        ),
        insurance_update_data: InsuranceUpdateResource = Body(
            default=...,
            title="InsuranceUpdateResource",
            description="""The data for the insurance to update."""
        ),
        session: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_employee_token)
):
    return handle_http_exception(
        error_message="Failed to update insurance in the MySQL Employee database",
        callback=lambda: service.update(
            session,
            token_payload,
            str(insurance_id),
            insurance_update_data
        )
    )