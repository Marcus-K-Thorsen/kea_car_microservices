from .publishers import (
    employee_created_publisher,
    employee_updated_publisher,
    employee_deleted_publisher,
    employee_undeleted_publisher
)
from .base_publisher import BaseModel, Union, BaseEntity


def publish_employee_created_message(message: Union[str, bytes, dict, list, BaseModel, BaseEntity]) -> None:
    employee_created_publisher.publish(message)

def publish_employee_updated_message(message: Union[str, bytes, dict, list, BaseModel, BaseEntity]) -> None:
    employee_updated_publisher.publish(message)

def publish_employee_deleted_message(message: Union[str, bytes, dict, list, BaseModel, BaseEntity]) -> None:
    employee_deleted_publisher.publish(message)
    
def publish_employee_undeleted_message(message: Union[str, bytes, dict, list, BaseModel, BaseEntity]) -> None:
    employee_undeleted_publisher.publish(message)
    

def close_all_connections() -> None:
    employee_created_publisher.close_connection()
    employee_updated_publisher.close_connection()
    employee_deleted_publisher.close_connection()
    employee_undeleted_publisher.close_connection()



