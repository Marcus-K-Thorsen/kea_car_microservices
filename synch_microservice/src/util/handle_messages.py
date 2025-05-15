# External Library imports

# Internal Library import
from src.util.handle_insurance_message import handle_insurance_message
from src.database_management import Database
from src.entities import InsuranceMessage
from src.logger_tool import logger


def handle_message(database: Database, message: dict, routing_key: str) -> None:
    if not isinstance(database, Database):
        logger.error(f"Invalid database type: {type(database).__name__}. Expected Database.")
        raise TypeError(f"database must be of type Database, not {type(database).__name__}.")
    
    if not isinstance(message, dict):
        logger.error(f"Invalid message type: {type(message).__name__}. Expected dict.")
        raise TypeError(f"message must be of type dict, not {type(message).__name__}.")
    
    if not isinstance(routing_key, str):
        logger.error(f"Invalid routing key type: {type(routing_key).__name__}. Expected str.")
        raise TypeError(f"routing_key must be of type str, not {type(routing_key).__name__}.")
    
    _id = message.pop("id", None)
    
    if not isinstance(_id, str):
        logger.error(f"Invalid id type: {type(_id).__name__}. Expected str.")
        raise TypeError(f"id must be of type str, not {type(_id).__name__}.")
    
    if "insurance" in routing_key:
        logger.info(f"Handling insurance message with routing key: {routing_key}")
        insurance_message = InsuranceMessage(_id=_id, **message)
        handle_insurance_message(database, insurance_message, routing_key)
    else:
        raise ValueError(f"Invalid routing key: {routing_key}, expected 'insurance' in routing key.")