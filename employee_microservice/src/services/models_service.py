# External Library imports
from typing import List, Optional

# Internal library imports
from src.logger_tool import logger
from src.entities import BrandEntity
from src.database_management import Session
from src.resources import ModelReturnResource
from src.exceptions import UnableToFindIdError
from src.core import TokenPayload, get_current_employee
from src.repositories import ModelRepository, BrandRepository


def get_all(
        session: Session,
        token: TokenPayload,
        brand_id: Optional[str] = None,
        model_limit: Optional[int] = None
) -> List[ModelReturnResource]:

    model_repository = ModelRepository(session)
    
    if not (isinstance(brand_id, str) or brand_id is None):
        raise TypeError(f"brand_id must be of type str or None, "
                        f"not {type(brand_id).__name__}.")
    if isinstance(model_limit, bool) or not (isinstance(model_limit, int) or model_limit is None):
        raise TypeError(f"model_limit must be of type int or None, "
                        f"not {type(model_limit).__name__}.")

    get_current_employee(
        token,
        session,
        current_user_action="get_all models"
    )
    
    brand_entity: Optional[BrandEntity] = None
    if brand_id is not None:
        brand_repository = BrandRepository(session)
        brand_entity = brand_repository.get_by_id(brand_id)
        if brand_entity is None:
            raise UnableToFindIdError(
                entity_name="Brand",
                entity_id=brand_id
            )

    models = model_repository.get_all(brand_entity, model_limit)
    return [model.as_resource() for model in models]


def get_by_id(
        session: Session,
        token: TokenPayload,
        model_id: str
) -> ModelReturnResource:
    
    repository = ModelRepository(session)
    
    if not isinstance(model_id, str):
        raise TypeError(f"model_id must be of type str, "
                        f"not {type(model_id).__name__}.")
    
    get_current_employee(
        token,
        session,
        current_user_action="get model by id"
    )

    model = repository.get_by_id(model_id)
    if model is None:
        raise UnableToFindIdError("Model", model_id)
    
    logger.info(f"Model as bytes: {model.to_bytes()}")
    
    return model.as_resource()

