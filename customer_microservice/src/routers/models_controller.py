"""
**Models Controller Module**

This module defines the FastAPI routes for model-related operations.
It provides endpoints to retrieve all car models or a specific car model by its ID.

Key Responsibilities:

- Define routes for car model-related API operations.
- Handle exceptions and return appropriate HTTP responses.
"""

# External Library imports
from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, Path, Query

# Internal library imports
from src.resources import ModelReturnResource
from src.exceptions import handle_http_exception
from src.services import models_service as service
from src.database_management import Database, get_mongodb


router: APIRouter = APIRouter()


def get_db():
    with get_mongodb() as database:
        yield database


@router.get(
    path="/models",
    response_model=List[ModelReturnResource],
    response_description=
    """
    Successfully retrieved a list of models.
    Returns: List[ModelReturnResource].
    """,
    summary="Retrieve Models.",
    description=
    """
    Retrieves all or a limited amount of Models from the Customer database 
    potentially filtered by models belonging to a brand 
    and returns a list of 'ModelReturnResource'.
    """
)
async def get_models(
        brand_id: Optional[UUID] = Query(
            default=None,
            description="""The UUID of the brand, to retrieve models belonging to that brand."""
        ),
        limit: Optional[int] = Query(
            default=None, ge=1,
            description="""Set a limit for the amount of models that is returned."""
        ),
        customer_database: Database = Depends(get_db)
):
    """
    Retrieves a list of car models from the database.

    :param brand_id: The UUID of the brand to filter models by (optional).
    :type brand_id: UUID | None
    :param limit: The maximum number of car models to retrieve (optional).
    :type limit: int | None
    :param customer_database: The database connection dependency.
    :type customer_database: Database
    :return: A list of models as `ModelReturnResource`.
    :rtype: List[ModelReturnResource]
    """
    return handle_http_exception(
        error_message="Failed to get models from the Customer database",
        callback=lambda: service.get_all(
            database=customer_database,
            brand_id=None if not brand_id else str(brand_id),
            models_limit=limit
        )
    )


@router.get(
    path="/models/{model_id}",
    response_model=ModelReturnResource,
    response_description=
    """
    Successfully retrieved a model.
    Returns: ModelReturnResource.
    """,
    summary="Retrieve a Model by ID.",
    description=
    """
    Retrieves a car Model by ID from the Customer database 
    by giving a UUID in the path for the model 
    and returns it as a 'ModelReturnResource'.
    """
)
async def get_model(
        model_id: UUID = Path(
            default=...,
            description="""The UUID of the model to retrieve."""
        ),
        customer_database: Database = Depends(get_db)
):
    """
    Retrieves a specific car model by its UUID.

    :param model_id: The UUID of the car model to retrieve.
    :type model_id: UUID
    :param customer_database: The database connection dependency.
    :type customer_database: Database
    :return: The model as a `ModelReturnResource`.
    :rtype: ModelReturnResource
    """
    return handle_http_exception(
        error_message="Failed to get model from the Customer database",
        callback=lambda: service.get_by_id(
            database=customer_database,
            model_id=str(model_id)
        )
    )
