# External Library imports

# Internal Library import
from src.logger_tool import logger
import src.services.models_service as service
from src.entities import ModelMessage
from src.database_management import Database

def handle_model_message(database: Database, model_message: ModelMessage, routing_key: str) -> None:
    
    if "create" in routing_key:
        logger.info(f"Handling model creation with routing key: {routing_key}")
        service.create(database, model_message)
        logger.info(f"Model created with ID: {model_message.id}")
    else:
        logger.error(f"Invalid routing key: {routing_key}, expected one of either ['create', 'update'] in routing key.")
        raise ValueError(f"Invalid routing key: {routing_key}, expected one of either ['create', 'update'] in routing key.")
