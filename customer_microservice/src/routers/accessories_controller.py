# External Library imports
from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, Path, Query

# Internal library imports
from src.exceptions import handle_http_exception
from src.resources import AccessoryReturnResource
from mongodb_connection import Database, get_mongodb
from src.services import accessories_service as service


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
    return handle_http_exception(
        error_message="Failed to get accessory from the Customer database",
        callback=lambda: service.get_by_id(
            database=customer_database,
            accessory_id=str(accessory_id)
        )
    )
