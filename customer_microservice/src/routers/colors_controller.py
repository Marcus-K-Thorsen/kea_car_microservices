"""
**Colors Controller Module**

This module defines the FastAPI routes for color-related operations.
It provides endpoints to retrieve all colors or a specific color by its ID.

Key Responsibilities:

- Define routes for color-related API operations.
- Handle exceptions and return appropriate HTTP responses.
"""

# External Library imports
from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, Path, Query

# Internal library imports
from src.resources import ColorReturnResource
from src.exceptions import handle_http_exception
from src.services import colors_service as service
from src.database_management import Database, get_mongodb


router: APIRouter = APIRouter()


def get_db():
    with get_mongodb() as database:
        yield database


@router.get(
    path="/colors",
    response_model=List[ColorReturnResource],
    response_description=
    """
    Successfully retrieved a list of colors.
    Returns: List[ColorReturnResource].
    """,
    summary="Retrieve Colors.",
    description=
    """
    Retrieves all or a limited amount of Colors from the 
    Customer database and returns a list of 'ColorReturnResource'.
    """
)
async def get_colors(
        limit: Optional[int] = Query(
            default=None, ge=1,
            description="""Set a limit for the amount of colors that is returned."""
        ),
        customer_database: Database = Depends(get_db)
):
    """
    Retrieves a list of colors from the database.

    :param limit: The maximum number of colors to retrieve (optional).
    :type limit: int | None
    :param customer_database: The database connection dependency.
    :type customer_database: Database
    :return: A list of colors as `ColorReturnResource`.
    :rtype: List[ColorReturnResource]
    """
    return handle_http_exception(
        error_message="Failed to get colors from the Customer database",
        callback=lambda: service.get_all(
            database=customer_database,
            colors_limit=limit
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
    summary="Retrieve a Color by ID.",
    description=
    """
    Retrieves a Color by ID from the Customer database by giving a UUID 
    in the path for the color and returns it as a 'ColorReturnResource'.
    """
)
async def get_color(
        color_id: UUID = Path(
            default=...,
            description="""The UUID of the color to retrieve."""
        ),
        customer_database: Database = Depends(get_db)
):
    """
    Retrieves a specific color by its UUID.

    :param color_id: The UUID of the color to retrieve.
    :type color_id: UUID
    :param customer_database: The database connection dependency.
    :type customer_database: Database
    :return: The color as a `ColorReturnResource`.
    :rtype: ColorReturnResource
    """
    return handle_http_exception(
        error_message="Failed to get color from the Customer database",
        callback=lambda: service.get_by_id(
            database=customer_database,
            color_id=str(color_id)
        )
    )
