# External Library imports
from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, Path, Query

# Internal library imports
from src.core import get_current_employee_token, TokenPayload
from src.database_management import Session, get_mysqldb
from src.services import accessories_service as service
from src.exceptions import handle_http_exception
from src.resources import AccessoryReturnResource

router: APIRouter = APIRouter()

def get_db():
    with get_mysqldb() as session:
        yield session


@router.get(
    path="/accessories",
    response_model=List[AccessoryReturnResource],
    response_description=
    """
    Successfully retrieved a list of accessories.
    Returns: List[AccessoryReturnResource].
    """,
    summary="Retrieve Accessories - Requires authorization token in header.",
    description=
    """
    Retrieves all or a limited amount of Accessories from the 
    MySQL Employee database and returns a list of 'AccessoryReturnResource'.
    
    The endpoint requires an authorization token in the header and is accessible by all roles.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def get_accessories(
        limit: Optional[int] = Query(
            default=None, ge=1,
            description="""Set a limit for the amount of accessories that is returned."""
        ),
        session: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_employee_token)
):
    return await handle_http_exception(
        error_message="Failed to get accessories from the MySQL Employee database",
        callback=lambda: service.get_all(
            session,
            token_payload,
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
    summary="Retrieve an Accessory by ID - Requires authorization token in header.",
    description=
    """
    Retrieves an Accessory by ID from the MySQL employee database 
    by giving a UUID in the path for the accessory and 
    returns it as an 'AccessoryReturnResource'.
    
    The endpoint requires an authorization token in the header and is accessible by all roles.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def get_accessory(
        accessory_id: UUID = Path(
            default=...,
            description="""The UUID of the accessory to retrieve."""
        ),
        session: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_employee_token)
):
    return await handle_http_exception(
        error_message="Failed to get accessory from the MySQL Employee database",
        callback=lambda: service.get_by_id(
            session,
            token_payload,
            accessory_id=str(accessory_id)
        )
    )
