# External Library imports
from typing import Optional, List

# Internal library imports
from src.repositories.base_repository import BaseRepository
from src.entities import ModelMessage, ModelEntity, ColorEntity, BrandEntity


class ModelRepository(BaseRepository):
    def get_by_id(self, model_id: str) -> Optional[ModelEntity]:
        """
        Retrieves a specific model by its ID from the Customer Mongo database.

        This method queries the MongoDB collection for a model with the given ID
        and returns it as an `ModelEntity` object. If no model is found, it
        returns `None`.

        :param model_id: The ID of the model to retrieve.
        :type model_id: str
        :return: The `ModelEntity` object if found, otherwise `None`.
        :rtype: ModelEntity | None
        """
        models_collection = self.get_models_collection()
        model_query = models_collection.find_one({"_id": model_id})
        
        if model_query is not None:
            return ModelEntity(**model_query)
        return None
    
    def create(self, 
               model_create_data: ModelMessage, 
               brand_entity: BrandEntity, 
               color_entities: List[ColorEntity]
        ) -> ModelEntity:
        """
        Creates a new model in the Customer Mongo database.
        
        :param model_create_data: The data for the model to create.
        :type model_create_data: ModelMessage
        :return: The created model entity.
        :rtype: ModelEntity
        """
        models_collection = self.get_models_collection()
        model_entity = ModelEntity(
            _id=model_create_data.id,
            name=model_create_data.name,
            price=model_create_data.price,
            image_url=model_create_data.image_url,
            brand=brand_entity,
            colors=color_entities,
            created_at=model_create_data.created_at,
            updated_at=model_create_data.updated_at
        )
        
        models_collection.insert_one(model_entity.to_mongo_dict(exlude_id=False))
        return model_entity
        
    
    