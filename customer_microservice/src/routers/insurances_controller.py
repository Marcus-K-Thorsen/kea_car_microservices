# External Library imports
from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, Path, Query

# Internal library imports
from src.exceptions import handle_http_exception
from src.resources import InsuranceReturnResource
from src.services import insurances_service as service
from src.database_management import Database, get_mongodb


router: APIRouter = APIRouter()

def get_db():
    with get_mongodb() as database:
        yield database



@router.get(
    path="/insurances",
    response_model=List[InsuranceReturnResource],
    response_description=
    """
    Successfully retrieved a list of insurances.
    Returns: List[InsuranceReturnResource].
    """,
    summary="Retrieve Insurances.",
    description=
    """
    Retrieves all or a limited amount of Insurances from the 
    Customer database and returns a list of 'InsuranceReturnResource'.
    """
)
async def get_insurances(
        limit: Optional[int] = Query(
            default=None, ge=1,
            description="""Set a limit for the amount of insurances that is returned."""
        ),
        customer_database: Database = Depends(get_db)
):
    return handle_http_exception(
        error_message="Failed to get insurances from the Customer database",
        callback=lambda: service.get_all(
            database=customer_database,
            insurances_limit=limit
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
    summary="Retrieve an Insurance by ID.",
    description=
    """
    Retrieves an Insurance by ID from the Customer database 
    by giving a UUID in the path for the insurance 
    and returns it as an 'InsuranceReturnResource'.
    """
)
async def get_insurance(
        insurance_id: UUID = Path(
            default=...,
            description="""The UUID of the insurance to retrieve."""
        ),
        customer_database: Database = Depends(get_db)
):
    return handle_http_exception(
        error_message="Failed to get insurance from the Customer database",
        callback=lambda: service.get_by_id(
            database=customer_database,
            insurance_id=str(insurance_id)
        )
    )
