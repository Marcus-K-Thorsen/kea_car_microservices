# External Library imports


# Internal Library import
from src.util.handle_employee_message import handle_employee_message
from src.database_management import Session
from src.entities.employee import EmployeeMesssage
from src.logger_tool import logger


def handle_message(session: Session, message: dict, routing_key: str) -> None:
    if not isinstance(session, Session):
        logger.error(f"Invalid session type: {type(session).__name__}. Expected Session.")
        raise TypeError(f"session must be of type Session, not {type(session).__name__}.")
    
    if not isinstance(message, dict):
        logger.error(f"Invalid message type: {type(message).__name__}. Expected dict.")
        raise TypeError(f"message must be of type dict, not {type(message).__name__}.")
    
    if not isinstance(routing_key, str):
        logger.error(f"Invalid routing key type: {type(routing_key).__name__}. Expected str.")
        raise TypeError(f"routing_key must be of type str, not {type(routing_key).__name__}.")
    
    if "employee" in routing_key:
        logger.info(f"Handling employee message with routing key: {routing_key}")
        employee_message = EmployeeMesssage(**message)
        handle_employee_message(session, employee_message, routing_key)
        session.commit()
    else:
        raise ValueError(f"Invalid routing key: {routing_key}, expected 'employee' in routing key.")