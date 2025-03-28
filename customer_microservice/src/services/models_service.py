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

    repository = ModelRepository(database)
    
    if not isinstance(model_id, str):
        raise TypeError(f"model_id must be of type str, "
                        f"not {type(model_id).__name__}.")

    model = repository.get_by_id(model_id)
    
    if model is None:
        raise UnableToFindIdError("Model", model_id)
    
    return model.as_resource()
