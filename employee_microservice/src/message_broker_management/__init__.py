# External Library imports


# Internal Library imports
from .main_consumer import start_consumer, stop_consumer, get_admin_exchange_consumer

from .publishers import (
    insurance_created_publisher,
    insurance_updated_publisher
)
from .base_publisher import BaseModel, Union, BaseEntity


def publish_insurance_created_message(message: Union[str, bytes, dict, list, BaseModel, BaseEntity]) -> None:
    insurance_created_publisher.publish(message)

def publish_insurance_updated_message(message: Union[str, bytes, dict, list, BaseModel, BaseEntity]) -> None:
    insurance_updated_publisher.publish(message)


def close_all_publisher_connections() -> None:
    insurance_created_publisher.close_connection()
    insurance_updated_publisher.close_connection()

