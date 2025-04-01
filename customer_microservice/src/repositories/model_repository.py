"""
**Model Repository Module**

This module defines the `ModelRepository` class, which provides methods for interacting
with the MongoDB collection for car models. It extends the `BaseRepository` class and
implements model-specific database operations.

Key Responsibilities:

- Retrieve all car models with optional filters and limits.
- Retrieve a specific car model by its ID.
"""

# External Library imports
from typing import Optional, List, Dict, Any
from pymongo.cursor import Cursor

# Internal library imports
from src.repositories.base_repository import BaseRepository
from src.entities import ModelEntity, BrandEntity, ColorEntity


class ModelRepository(BaseRepository):
    """
    Repository for managing car model-related database operations.

    This class provides methods to interact with the MongoDB collection for car models,
    including retrieving all models or a specific model by its ID.
    """

    def get_all(self,
                brand_entity: Optional[BrandEntity] = None,
                limit: Optional[int] = None
                ) -> List[ModelEntity]:
        """
        Retrieves all car models from the database, with optional filters and limits.

        This method queries the MongoDB collection for car models and returns a list
        of `ModelEntity` objects. If a `brand_entity` is provided, the results are
        filtered to include only models associated with that brand. If a limit is
        provided, the number of results is restricted to the specified value.

        :param brand_entity: The brand to filter models by (optional).
        :type brand_entity: Optional[BrandEntity]
        :param limit: The maximum number of models to retrieve (optional).
        :type limit: int | None
        :return: A list of `ModelEntity` objects.
        :rtype: List[ModelEntity]
        """
        models_collection = self.get_models_collection()
        models_query: Cursor[Dict[str, Any]]
        
        if brand_entity is not None and isinstance(brand_entity, BrandEntity):
            models_query = models_collection.find({"brand._id": brand_entity.id})
        else:
            models_query = models_collection.find()
        
        if self.limit_is_valid(limit):
            models_query = models_query.limit(limit)
        
        retrieved_models: List[ModelEntity] = []
        for model in models_query:
            brand = BrandEntity(**model.get("brand"))
            colors = [ColorEntity(**color) for color in model.get("colors")]
            model.update({"brand": brand, "colors": colors})
            retrieved_model = ModelEntity(**model)
            retrieved_models.append(retrieved_model)

        return retrieved_models

    def get_by_id(self, model_id: str) -> Optional[ModelEntity]:
        """
        Retrieves a specific car model by its ID.

        This method queries the MongoDB collection for a car model with the given ID
        and returns it as a `ModelEntity` object. If no model is found, it returns `None`.

        :param model_id: The ID of the car model to retrieve.
        :type model_id: str
        :return: The `ModelEntity` object if found, otherwise `None`.
        :rtype: ModelEntity | None
        """
        models_collection = self.get_models_collection()
        model_query = models_collection.find_one({"_id": model_id})
        if model_query is not None:
            return ModelEntity(**model_query)
        return None
