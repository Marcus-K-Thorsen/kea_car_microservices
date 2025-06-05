# External Library imports
from typing import Optional
# Internal Library imports
from .publishers import (
    EmployeeCreatedPublisher,
    EmployeeUpdatedPublisher,
    EmployeeDeletedPublisher,
    EmployeeUndeletedPublisher
)
from .base_publisher import BaseModel, Union, BaseEntity


def publish_employee_created_message(message: Union[str, bytes, dict, list, BaseModel, BaseEntity]) -> None:
    employee_created_publisher: Optional[EmployeeCreatedPublisher] = None
    try:
        employee_created_publisher = EmployeeCreatedPublisher()
        employee_created_publisher.publish(message)
    finally:
        if employee_created_publisher:
            employee_created_publisher.close_connection()

def publish_employee_updated_message(message: Union[str, bytes, dict, list, BaseModel, BaseEntity]) -> None:
    employee_updated_publisher: Optional[EmployeeUpdatedPublisher] = None
    try:
        employee_updated_publisher = EmployeeUpdatedPublisher()
        employee_updated_publisher.publish(message)
    finally:
        if employee_updated_publisher:
            employee_updated_publisher.close_connection()

def publish_employee_deleted_message(message: Union[str, bytes, dict, list, BaseModel, BaseEntity]) -> None:
    employee_deleted_publisher: Optional[EmployeeDeletedPublisher] = None
    try:
        employee_deleted_publisher = EmployeeDeletedPublisher()
        employee_deleted_publisher.publish(message)
    finally:
        if employee_deleted_publisher:
            employee_deleted_publisher.close_connection()
    
def publish_employee_undeleted_message(message: Union[str, bytes, dict, list, BaseModel, BaseEntity]) -> None:
    employee_undeleted_publisher: Optional[EmployeeUndeletedPublisher] = None
    try:
        employee_undeleted_publisher = EmployeeUndeletedPublisher()
        employee_undeleted_publisher.publish(message)
    finally:
        if employee_undeleted_publisher:
            employee_undeleted_publisher.close_connection()



