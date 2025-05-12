# External Library imports

# Internal Library import
from src.logger_tool import logger
import src.services.employees_service as service
from src.entities.employee import EmployeeEntity
from src.database_management import Database

def handle_employee_message(database: Database, employee_message: EmployeeEntity, routing_key: str) -> None:
    
    if "create" in routing_key:
        logger.info(f"Handling employee creation with routing key: {routing_key}")
        service.create(database, employee_message)
        logger.info(f"Employee created with ID: {employee_message.id}")
    elif "update" in routing_key:
        logger.info(f"Handling employee update with routing key: {routing_key}")
        service.update(database, employee_message)
        logger.info(f"Employee updated with ID: {employee_message.id}")
    elif "undelete" in routing_key:
        logger.info(f"Handling employee undelete with routing key: {routing_key}")
        service.undelete(database, employee_message)
        logger.info(f"Employee undeleted with ID: {employee_message.id}")
    elif "delete" in routing_key:
        logger.info(f"Handling employee deletion with routing key: {routing_key}")
        service.delete(database, employee_message)
        logger.info(f"Employee deleted with ID: {employee_message.id}")
    else:
        logger.error(f"Invalid routing key: {routing_key}, expected one of either ['create', 'update', 'delete', 'undelete'] in routing key.")
        raise ValueError(f"Invalid routing key: {routing_key}, expected one of either ['create', 'update', 'delete', 'undelete'] in routing key.")
