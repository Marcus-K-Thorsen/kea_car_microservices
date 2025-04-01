"""
**Insurances Controller Module**

This module defines the FastAPI routes for insurance-related operations.
It provides endpoints to retrieve all insurances or a specific insurance by its ID.

Key Responsibilities:

- Define routes for insurance-related API operations.
- Handle exceptions and return appropriate HTTP responses.
"""

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
    """
    Retrieves a list of insurances from the database.

    :param limit: The maximum number of insurances to retrieve (optional).
    :type limit: int | None
    :param customer_database: The database connection dependency.
    :type customer_database: Database
    :return: A list of insurances as `InsuranceReturnResource`.
    :rtype: List[InsuranceReturnResource]
    """
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
    """
    Retrieves a specific insurance by its UUID.

    :param insurance_id: The UUID of the insurance to retrieve.
    :type insurance_id: UUID
    :param customer_database: The database connection dependency.
    :type customer_database: Database
    :return: The insurance as an `InsuranceReturnResource`.
    :rtype: InsuranceReturnResource
    """
    return handle_http_exception(
        error_message="Failed to get insurance from the Customer database",
        callback=lambda: service.get_by_id(
            database=customer_database,
            insurance_id=str(insurance_id)
        )
    )
