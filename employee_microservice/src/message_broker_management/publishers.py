# Internal library imports
from src.message_broker_management.base_publisher import BasePublisher
from typing import Optional
from .base_publisher import BaseModel, Union, BaseEntity



class InsuranceCreatedPublisher(BasePublisher):
    def __init__(self):
        super().__init__(routing_key="insurance.created")
        

class InsuranceUpdatedPublisher(BasePublisher):
    def __init__(self):
        super().__init__(routing_key="insurance.updated")

def publish_insurance_created_message(message: Union[str, bytes, dict, list, BaseModel, BaseEntity]) -> None:
    insurance_created_publisher: Optional[InsuranceCreatedPublisher] = None
    try:
        insurance_created_publisher = InsuranceCreatedPublisher()
        insurance_created_publisher.publish(message)
    finally:
        if insurance_created_publisher:
            insurance_created_publisher.close_connection()

def publish_insurance_updated_message(message: Union[str, bytes, dict, list, BaseModel, BaseEntity]) -> None:
    insurance_updated_publisher: Optional[InsuranceUpdatedPublisher] = None
    try:
        insurance_updated_publisher = InsuranceUpdatedPublisher()
        insurance_updated_publisher.publish(message)
    finally:
        if insurance_updated_publisher:
            insurance_updated_publisher.close_connection()
            

class ModelCreatedPublisher(BasePublisher):
    def __init__(self):
        super().__init__(routing_key="model.created")
        

def publish_model_created_message(message: Union[str, bytes, dict, list, BaseModel, BaseEntity]) -> None:
    model_created_publisher: Optional[ModelCreatedPublisher] = None
    try:
        model_created_publisher = ModelCreatedPublisher()
        model_created_publisher.publish(message)
    finally:
        if model_created_publisher:
            model_created_publisher.close_connection()

