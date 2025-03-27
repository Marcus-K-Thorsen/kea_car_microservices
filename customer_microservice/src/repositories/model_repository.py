# External Library imports
from typing import Optional, List, Dict, Any
from pymongo.cursor import Cursor


# Internal library imports
from src.repositories.base_repository import BaseRepository
from src.entities import ModelEntity, BrandEntity, ColorEntity


class ModelRepository(BaseRepository):
    
    def get_all(self,
                brand_entity: Optional[BrandEntity] = None,
                limit: Optional[int] = None
                ) -> List[ModelEntity]:
        
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
        models_collection = self.get_models_collection()
        model_query = models_collection.find_one({"_id": model_id})
        if model_query is not None:
            return ModelEntity(**model_query)
        return None