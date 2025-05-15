# External Library imports
from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, Path, Query

# Internal library imports
from src.resources import ModelReturnResource, ModelCreateResource
from src.core import get_current_employee_token, TokenPayload
from src.database_management import Session, get_mysqldb
from src.services import models_service as service
from src.exceptions import handle_http_exception



router: APIRouter = APIRouter()

def get_db():
    with get_mysqldb() as session:
        yield session


@router.get(
    path="/models",
    response_model=List[ModelReturnResource],
    response_description=
    """
    Successfully retrieved a list of models.
    Returns: List[ModelReturnResource].
    """,
    summary="Retrieve Models - Requires authorization token in header.",
    description=
    """
    Retrieves all or a limited amount of Models from the 
    MySQL Employee database potentially filtered by models belonging 
    to a brand and returns a list of 'ModelReturnResource'.
    
    The endpoint requires an authorization token in the header and is accessible by all roles.
    """,
    dependencies=[Depends(get_current_employee_token)]
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
        session: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_employee_token)
):
    return handle_http_exception(
        error_message="Failed to get models from the MySQL Employee database",
        callback=lambda: service.get_all(
            session,
            token_payload,
            brand_id=None if not isinstance(brand_id, UUID) else str(brand_id),
            model_limit=limit
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
    summary="Retrieve a Model by ID - Requires authorization token in header.",
    description=
    """
    Retrieves a Model by ID from the MySQL Employee database 
    by giving a UUID in the path for the model 
    and returns it as a 'ModelReturnResource'.
    
    The endpoint requires an authorization token in the header and is accessible by all roles.
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def get_model(
        model_id: UUID = Path(
            default=...,
            description="""The UUID of the model to retrieve."""
        ),
        session: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_employee_token)
):
    return handle_http_exception(
        error_message="Failed to get model from the MySQL Employee database",
        callback=lambda: service.get_by_id(
            session,
            token_payload,
            model_id=str(model_id)
        )
    )
    
