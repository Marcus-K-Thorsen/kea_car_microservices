# External Library imports
from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, Path, Query

# Internal library imports
from src.resources import BrandReturnResource
from src.exceptions import handle_http_exception
from src.services import brands_service as service
from src.database_management import Database, get_mongodb


router: APIRouter = APIRouter()


def get_db():
    with get_mongodb() as database:
        yield database



@router.get(
    path="/brands",
    response_model=List[BrandReturnResource],
    response_description=
    """
    Successfully retrieved a list of brands.
    Returns: List[BrandReturnResource].
    """,
    summary="Retrieve Brands.",
    description=
    """
    Retrieves all or a limited amount of Brands from the 
    Customer database and returns a list of 'BrandReturnResource'.
    """
)
async def get_brands(
        limit: Optional[int] = Query(
            default=None, ge=1,
            description="""Set a limit for the amount of brands that is returned."""
        ),
        customer_database: Database = Depends(get_db)
):
    return handle_http_exception(
        error_message="Failed to get brands from the Customer database",
        callback=lambda: service.get_all(
            database=customer_database,
            brands_limit=limit
        )
    )


@router.get(
    path="/brands/{brand_id}",
    response_model=BrandReturnResource,
    response_description=
    """
    Successfully retrieved a brand. 
    Returns: BrandReturnResource.
    """,
    summary="Retrieve a Brand by ID.",
    description=
    """
    Retrieves a Brand by ID from the Customer database by giving a UUID 
    in the path for the brand and returns it as a 'BrandReturnResource'.
    """
)
async def get_brand(
        brand_id: UUID = Path(
            default=...,
            description="""The UUID of the brand to retrieve."""
        ),
        customer_database: Database = Depends(get_db)
):
    return handle_http_exception(
        error_message="Failed to get brand from the Customer database",
        callback=lambda: service.get_by_id(
            database=customer_database,
            brand_id=str(brand_id)
        )
    )

