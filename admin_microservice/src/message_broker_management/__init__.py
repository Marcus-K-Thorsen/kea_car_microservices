from .publishers import (
    EmployeeCreatedPublisher,
    EmployeeUpdatedPublisher,
    EmployeeDeletedPublisher,
    TrialPublisher,
    employee_created_publisher,
    employee_updated_publisher,
    employee_deleted_publisher,
    trial_publisher
)
from .base_publisher import BaseModel, Union


def publish_employee_created_message(message: Union[str, bytes, dict, list, BaseModel]) -> None:
    employee_created_publisher.publish(message)

def publish_employee_updated_message(message: Union[str, bytes, dict, list, BaseModel]) -> None:
    employee_updated_publisher.publish(message)

def publish_employee_deleted_message(message: Union[str, bytes, dict, list, BaseModel]) -> None:
    employee_deleted_publisher.publish(message)
    
def publish_trial_message(message: Union[str, bytes, dict, list, BaseModel]) -> None:
    trial_publisher.publish(message)


def close_all_connections() -> None:
    employee_created_publisher.close_connection()
    employee_updated_publisher.close_connection()
    employee_deleted_publisher.close_connection()
    trial_publisher.close_connection()



