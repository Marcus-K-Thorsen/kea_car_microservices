# External Library imports
from typing import List

# Internal library imports
from src.logger_tool import logger
from src.entities import ModelMessage, ColorEntity
from src.database_management import Database
from src.repositories import ModelRepository, ColorRepository, BrandRepository
from src.exceptions import AlreadyTakenFieldValueError, UnableToFindIdError


def create(
        database: Database,
        model_create_data: ModelMessage
) -> None:

    model_repository = ModelRepository(database)
    color_repository = ColorRepository(database)
    brand_repository = BrandRepository(database)
    
    if not isinstance(model_create_data, ModelMessage):
        raise TypeError(f"model_create_data must be of type ModelMessage, "
                        f"not {type(model_create_data).__name__}.")
    
    already_created_model = model_repository.get_by_id(model_create_data.id)
    if already_created_model is not None:
        logger.warning(f"Model with id {model_create_data.id} already exists.")
        logger.info("Will assume the model is already created, and this is a duplicate message and will drop it.")
        return None
    
    brand_entity = brand_repository.get_by_id(model_create_data.brand_id)
    if brand_entity is None:
        logger.warning(f"Brand with id {model_create_data.brand_id} not found.")
        logger.error("Unable to create model due to missing brand, will assume the brand has not been created yet and will therefore reque the model create message.")
        raise UnableToFindIdError("Brand", model_create_data.brand_id)
    
    color_entities: List[ColorEntity] = []
    for color_id in model_create_data.colors_ids:
        color_entity = color_repository.get_by_id(color_id)
        if color_entity is None:
            logger.warning(f"Color with id {color_id} not found.")
            logger.error("Unable to create model due to missing color, will assume the color has not been created yet and will therefore reque the model create message.")
            raise UnableToFindIdError("Color", color_id)
        color_entities.append(color_entity)
        
    model_repository.create(
        model_create_data,
        brand_entity,
        color_entities
    )
    return None


