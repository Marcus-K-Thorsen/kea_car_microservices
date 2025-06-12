# External Library imports
import os
import boto3
from datetime import datetime
from botocore.client import Config, BaseClient
from dotenv import load_dotenv
from fastapi import UploadFile
from typing import List, Optional

# Internal library imports
from src.logger_tool import logger
from src.entities import BrandEntity
from src.database_management import Session
from src.message_broker_management import publish_model_created_message
from src.resources import ModelReturnResource, ModelCreateResource, RoleEnum
from src.repositories import ModelRepository, BrandRepository, ColorRepository
from src.core import TokenPayload, get_current_employee, is_invalid_mime_type, read_file_if_within_size_limit
from src.exceptions import UnableToFindIdError, FileIsNotCorrectFileTypeError, FileTooLargeError, FileCannotBeEmptyError

# Load environment variables from .env file
load_dotenv()

DIGITAL_OCEAN_SPACES_KEY = os.getenv("DIGITAL_OCEAN_SPACES_KEY")
DIGITAL_OCEAN_SPACES_SECRET = os.getenv("DIGITAL_OCEAN_SPACES_SECRET")
DIGITAL_OCEAN_SPACES_REGION = os.getenv("DIGITAL_OCEAN_SPACES_REGION")
DIGITAL_OCEAN_SPACES_BUCKET = os.getenv("DIGITAL_OCEAN_SPACES_BUCKET")
DIGITAL_OCEAN_SPACES_ENDPOINT = f"https://{DIGITAL_OCEAN_SPACES_REGION}.digitaloceanspaces.com"

VALID_MODEL_FILE_TYPES = ["image/png", "image/svg", "image/jpeg"]
MAX_MODEL_IMAGE_SIZE = 3 * 1024 * 1024  # 3MB

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
    
    return model.as_resource()


async def create(
        session: Session,
        token: TokenPayload,
        model_create_data: ModelCreateResource,
        model_image: UploadFile
) -> ModelReturnResource:
    
    model_repository = ModelRepository(session)
    brand_repository = BrandRepository(session)
    color_repository = ColorRepository(session)
    
    if not isinstance(model_create_data, ModelCreateResource):
        raise TypeError(f"model_create_data must be of type ModelCreateResource, "
                        f"not {type(model_create_data).__name__}.")
    
    get_current_employee(
        token,
        session,
        current_user_action="creating a model",
        valid_roles=[RoleEnum.admin, RoleEnum.manager]
    )

    already_created_model = model_repository.get_by_id(model_create_data.id)
    if already_created_model is not None:
        return already_created_model.as_resource()
    
    brand_entity = brand_repository.get_by_id(model_create_data.brands_id)
    if brand_entity is None:
        raise UnableToFindIdError(
            entity_name="Brand",
            entity_id=model_create_data.brands_id
        )
        
    color_entities: List[BrandEntity] = []
    for color_id in model_create_data.color_ids:
        color_entity = color_repository.get_by_id(color_id)
        if color_entity is None:
            raise UnableToFindIdError(
                entity_name="Color",
                entity_id=color_id
            )
        color_entities.append(color_entity)
    
    unique_filename = _get_unique_filename(model_image)
    
    if is_invalid_mime_type(model_image, VALID_MODEL_FILE_TYPES):
        raise FileIsNotCorrectFileTypeError(
            file_name=model_image.filename,
            file_type=model_image.content_type,
            allowed_file_types=VALID_MODEL_FILE_TYPES
        )
        
        
    is_file_too_large = await read_file_if_within_size_limit(model_image, MAX_MODEL_IMAGE_SIZE)
        
    if is_file_too_large is None:
        raise FileTooLargeError(
            file_name=model_image.filename,
            max_mega_bytes_size=MAX_MODEL_IMAGE_SIZE
        )
    
    file_content = is_file_too_large
    
    model_image_url = _upload_file_to_digital_ocean_spaces(
        model_image,
        file_content,
        unique_filename
    )
    model = model_repository.create(
        model_create_data=model_create_data,
        model_image_url=model_image_url,
        brand_entity=brand_entity,
        color_entities=color_entities
    )
    
    model_as_resource = model.as_resource()
    
    publish_model_created_message(message=model)
    
    return model_as_resource



def _get_unique_filename(file: UploadFile) -> str:
    filename = file.filename
    if filename is None or filename.strip() == "":
        raise FileCannotBeEmptyError()
    safe_filename = filename.replace("/", "_").replace("\\", "_").replace(" ", "_")
    safe_filename = safe_filename.replace(":", "_").replace("?", "_").replace("*", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{timestamp}__{safe_filename}"


def _upload_file_to_digital_ocean_spaces(
    file: UploadFile,
    file_content: bytes,
    unique_filename: str
) -> str:
    try:
        # Set up boto3 client
        s3: BaseClient = boto3.client(
            's3',
            region_name=DIGITAL_OCEAN_SPACES_REGION,
            endpoint_url=DIGITAL_OCEAN_SPACES_ENDPOINT,
            aws_access_key_id=DIGITAL_OCEAN_SPACES_KEY,
            aws_secret_access_key=DIGITAL_OCEAN_SPACES_SECRET,
            config=Config(signature_version='s3v4')
        )
        s3.put_object(
            Bucket=DIGITAL_OCEAN_SPACES_BUCKET,
            Key=unique_filename,
            Body=file_content,
            ACL='public-read',  # so the file is accessible publicly
            ContentType=file.content_type
        )
        image_url = f"https://{DIGITAL_OCEAN_SPACES_BUCKET}.{DIGITAL_OCEAN_SPACES_REGION}.cdn.digitaloceanspaces.com/{unique_filename}"
        return image_url
    except Exception as e:
        logger.error(f"Failed to upload file to Digital Ocean Spaces: {e}")
        raise

