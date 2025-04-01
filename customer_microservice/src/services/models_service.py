"""
**Models Service Module**

This module provides business logic for car model-related operations.
It interacts with the `ModelRepository` and `BrandRepository` to retrieve data from the database
and transforms it into resource representations for API responses.

Key Responsibilities:

- Retrieve all car models with optional filters and limits.
- Retrieve a specific car model by its ID.
"""

# External Library imports
from typing import List, Optional

# Internal library imports
from src.database_management import Database
from src.resources import ModelReturnResource
from src.exceptions import UnableToFindIdError
from src.repositories import ModelRepository, BrandRepository


def get_all(
        database: Database,
        brand_id: Optional[str] = None,
        models_limit: Optional[int] = None
) -> List[ModelReturnResource]:
    """
    Retrieves all car models from the database, with optional filters and limits.

    This function interacts with the `ModelRepository` to fetch car model data
    and converts it into a list of `ModelReturnResource` objects. If a `brand_id`
    is provided, the results are filtered to include only models associated with
    that brand. If a limit is provided, the number of results is restricted to
    the specified value.

    :param database: The database connection instance.
    :type database: Database
    :param brand_id: The ID of the brand to filter models by (optional).
    :type brand_id: str | None
    :param models_limit: The maximum number of models to retrieve (optional).
    :type models_limit: int | None
    :return: A list of models as `ModelReturnResource`.
    :rtype: List[ModelReturnResource]
    :raises TypeError: If `brand_id` is not of type `str` or `None`, or if `models_limit` is not of type `int` or `None`.
    :raises UnableToFindIdError: If the specified brand ID does not exist.
    """
    model_repository = ModelRepository(database)
    brand_repository = BrandRepository(database)
    
    if not (isinstance(brand_id, str) or brand_id is None):
        raise TypeError(f"brand_id must be of type str or None, "
                        f"not {type(brand_id).__name__}.")
        
    if isinstance(models_limit, bool) or not (isinstance(models_limit, int) or models_limit is None):
        raise TypeError(f"models_limit must be of type int or None, "
                        f"not {type(models_limit).__name__}.")

    brand_entity = None
    if brand_id is not None:
        brand_entity = brand_repository.get_by_id(brand_id)
        if brand_entity is None:
            raise UnableToFindIdError(
                entity_name="Brand",
                entity_id=brand_id
            )
    
    models = model_repository.get_all(brand_entity, limit=models_limit)
    
    return [model.as_resource() for model in models]


def get_by_id(
        database: Database,
        model_id: str
) -> ModelReturnResource:
    """
    Retrieves a specific car model by its ID.

    This function interacts with the `ModelRepository` to fetch a single car model
    and converts it into a `ModelReturnResource` object.

    :param database: The database connection instance.
    :type database: Database
    :param model_id: The ID of the model to retrieve.
    :type model_id: str
    :return: The model as a `ModelReturnResource`.
    :rtype: ModelReturnResource
    :raises TypeError: If `model_id` is not of type `str`.
    :raises UnableToFindIdError: If no model is found with the given ID.
    """
    repository = ModelRepository(database)
    
    if not isinstance(model_id, str):
        raise TypeError(f"model_id must be of type str, "
                        f"not {type(model_id).__name__}.")

    model = repository.get_by_id(model_id)
    
    if model is None:
        raise UnableToFindIdError("Model", model_id)
    
    return model.as_resource()
