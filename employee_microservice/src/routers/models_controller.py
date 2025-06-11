# External Library imports
from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, Path, Query, UploadFile, HTTPException, status
from PIL import Image
import io


# Internal library imports
from src.resources import ModelReturnResource, ModelCreateResource, model_as_form_with_file
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


ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg",}
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg"}
MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2MB

@router.post(
    path="/models",
    #response_model=ModelReturnResource,
    response_description=
    """
    Successfully created a model.
    Returns: ModelReturnResource.
    """,
    summary="Create a Model - Requires authorization token in header.",
    description=
    """
    Creates a Model within the MySQL Employee database 
    by giving a request body 'ModelCreateResource' 
    and returns it as a 'ModelReturnResource'.
    
    The endpoint requires an authorization token in the header and is only accessible by employees with the role: 'ADMIN' or 'MANAGER'.   
    """,
    dependencies=[Depends(get_current_employee_token)]
)
async def create_model(
        model_form_data: tuple[ModelCreateResource, UploadFile] = Depends(model_as_form_with_file),
        session: Session = Depends(get_db),
        token_payload: TokenPayload = Depends(get_current_employee_token)
):
    model_create_data, model_image = model_form_data
    # Check content type
    if model_image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image type. Only PNG and JPG/JPEG are allowed."
        )
    
    # Check extension
    ext = model_image.filename.lower().rsplit(".", 1)[-1]
    if f".{ext}" not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file extension. Only .png, .jpg, .jpeg are allowed."
        )
        
    # Check file size
    contents = await model_image.read()
    if len(contents) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image size exceeds 2MB limit."
        )
        
    # Check if file is a real image
    try:
        Image.open(io.BytesIO(contents)).verify()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is not a valid image."
        )
        
    # Reset file pointer for further use
    model_image.file.seek(0)
    
    

    return {"filename": model_image.filename, "content_type": model_image.content_type}