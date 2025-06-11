# External Library imports
from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, Path, Query

# Internal library imports
from src.core import get_current_employee_token, TokenPayload
from src.database_management import Session, get_mysqldb
from src.services import colors_service as service
from src.exceptions import handle_http_exception
from src.resources import ColorReturnResource


router: APIRouter = APIRouter()

def get_db():
    with get_mysqldb() as session:
        yield session


@router.get(
    path="/colors",
    response_model=List[ColorReturnResource],
    response_description=
    """
    Successfully retrieved a list of colors.
    Returns: List[ColorReturnResource].
    """,
    summary="Retrieve Colors - Requires authorization token in header.",
    description=
    """
    Retrieves all or a limited amount of Colors from the 
    MySQL Employee database and returns a list of 'ColorReturnResource'.
    
    The endpoint requires an authorization token in the header and is accessible by all roles.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def get_colors(
        limit: Optional[int] = Query(
            default=None, ge=1,
            description="""Set a limit for the amount of colors that is returned."""
        ),
        session: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_employee_token)
): 
    return await handle_http_exception(
        error_message="Failed to get colors from the MySQL Employee database",
        callback=lambda: service.get_all(
            session,
            token_payload,
            color_limit=limit
        )
    )


@router.get(
    path="/colors/{color_id}",
    response_model=ColorReturnResource,
    response_description=
    """
    Successfully retrieved a color.
    Returns: ColorReturnResource.
    """,
    summary="Retrieve a Color by ID - Requires authorization token in header.",
    description=
    """
    Retrieves a Color by ID from the MySQL Employee
    database and returns it as a 'ColorReturnResource'.
    
    The endpoint requires an authorization token in the header and is accessible by all roles.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def get_color(
        color_id: UUID = Path(
            default=...,
            description="""The UUID of the color to retrieve."""
        ),
        session: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_employee_token)
):
    return await handle_http_exception(
        error_message="Failed to get color from the MySQL Employee database",
        callback=lambda: service.get_by_id(
            session,
            token_payload,
            color_id=str(color_id)
        )
    )
