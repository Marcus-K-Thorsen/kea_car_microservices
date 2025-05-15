# External Library imports
from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, Path, Query

# Internal library imports
from src.core import get_current_employee_token, TokenPayload
from src.database_management import Session, get_mysqldb
from src.services import brands_service as service
from src.exceptions import handle_http_exception
from src.resources import BrandReturnResource


router: APIRouter = APIRouter()

def get_db():
    with get_mysqldb() as session:
        yield session


@router.get(
    path="/brands",
    response_model=List[BrandReturnResource],
    response_description=
    """
    Successfully retrieved a list of brands.
    Returns: List[BrandReturnResource].
    """,
    summary="Retrieve Brands - Requires authorization token in header.",
    description=
    """
    Retrieves all or a limited amount of Brands from the 
    MySQL Employee database and returns a list of 'BrandReturnResource'.
    
    The endpoint requires an authorization token in the header and is accessible by all roles.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def get_brands(
        limit: Optional[int] = Query(
            default=None, ge=1,
            description="""Set a limit for the amount of brands that is returned."""
        ),
        session: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_employee_token)
):
    return handle_http_exception(
        error_message="Failed to get brands from the MySQL Employee database",
        callback=lambda: service.get_all(
            session,
            token_payload,
            brand_limit=limit
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
    summary="Retrieve a Brand by ID - Requires authorization token in header.",
    description=
    """
    Retrieves a Brand by ID from the MySQL Employee database 
    by giving a UUID in the path for the brand 
    and returns it as a 'BrandReturnResource'.
    
    The endpoint requires an authorization token in the header and is accessible by all roles.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def get_brand(
        brand_id: UUID = Path(
            default=...,
            description="""The UUID of the brand to retrieve."""
        ),
        session: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_employee_token)
):
    return handle_http_exception(
        error_message="Failed to get brand from the MySQL Employee database",
        callback=lambda: service.get_by_id(
            session,
            token_payload,
            brand_id=str(brand_id)
        )
    )
    
