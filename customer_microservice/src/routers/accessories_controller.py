"""
**Accessories Controller Module**

This module defines the FastAPI routes for accessory-related operations.
It provides endpoints to retrieve all accessories or a specific accessory by its ID.

Key Responsibilities:

- Define routes for accessory-related API operations.
- Handle exceptions and return appropriate HTTP responses.
"""

# External Library imports
from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, Path, Query

# Internal library imports
from src.exceptions import handle_http_exception
from src.resources import AccessoryReturnResource
from src.services import accessories_service as service
from src.database_management import Database, get_mongodb


router: APIRouter = APIRouter()


def get_db():
    with get_mongodb() as database:
        yield database


@router.get(
    path="/accessories",
    response_model=List[AccessoryReturnResource],
    response_description=
    """
    Successfully retrieved a list of accessories.
    Returns: List[AccessoryReturnResource].
    """,
    summary="Retrieve Accessories.",
    description=
    """
    Retrieves all or a limited amount of Accessories from the 
    Customer database and returns a list of 'AccessoryReturnResource'.
    """
)
async def get_accessories(
        limit: Optional[int] = Query(
            default=None, ge=1,
            description="""Set a limit for the amount of accessories that is returned."""
        ),
        customer_database: Database = Depends(get_db)
):
    """
    Retrieves a list of accessories from the database.

    :param limit: The maximum number of accessories to retrieve (optional).
    :type limit: int | None
    :param customer_database: The database connection dependency.
    :type customer_database: Database
    :return: A list of accessories as `AccessoryReturnResource`.
    :rtype: List[AccessoryReturnResource]
    """
    return handle_http_exception(
        error_message="Failed to get accessories from the Customer database",
        callback=lambda: service.get_all(
            database=customer_database,
            accessory_limit=limit
        )
    )


@router.get(
    path="/accessories/{accessory_id}",
    response_model=AccessoryReturnResource,
    response_description=
    """
    Successfully retrieved an accessory.
    Returns: AccessoryReturnResource.
    """,
    summary="Retrieve an Accessory by ID.",
    description=
    """
    Retrieves an Accessory by ID from the Customer database 
    by giving a UUID in the path for the accessory and 
    returns it as an 'AccessoryReturnResource'.
    """
)
async def get_accessory(
        accessory_id: UUID = Path(
            default=...,
            description="""The UUID of the accessory to retrieve."""
        ),
        customer_database: Database = Depends(get_db)
):
    """
    Retrieves a specific accessory by its UUID.

    :param accessory_id: The UUID of the accessory to retrieve.
    :type accessory_id: UUID
    :param customer_database: The database connection dependency.
    :type customer_database: Database
    :return: The accessory as an `AccessoryReturnResource`.
    :rtype: AccessoryReturnResource
    """
    return handle_http_exception(
        error_message="Failed to get accessory from the Customer database",
        callback=lambda: service.get_by_id(
            database=customer_database,
            accessory_id=str(accessory_id)
        )
    )
