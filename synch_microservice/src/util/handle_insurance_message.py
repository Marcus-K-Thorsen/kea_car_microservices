# External Library imports

# Internal Library import
from src.logger_tool import logger
import src.services.insurances_service as service
from src.entities import InsuranceMessage
from src.database_management import Database

def handle_insurance_message(database: Database, insurance_message: InsuranceMessage, routing_key: str) -> None:
    
    if "create" in routing_key:
        logger.info(f"Handling insurance creation with routing key: {routing_key}")
        service.create(database, insurance_message)
        logger.info(f"Insurance created with ID: {insurance_message.id}")
    elif "update" in routing_key:
        logger.info(f"Handling insurance update with routing key: {routing_key}")
        service.update(database, insurance_message)
        logger.info(f"Insurance updated with ID: {insurance_message.id}")
    else:
        logger.error(f"Invalid routing key: {routing_key}, expected one of either ['create', 'update'] in routing key.")
        raise ValueError(f"Invalid routing key: {routing_key}, expected one of either ['create', 'update'] in routing key.")
