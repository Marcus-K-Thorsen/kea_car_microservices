
from pydantic import BaseModel
from typing import Union, Optional
from .rabbitmq_management import RabbitMQManagement
from src.logger_tool import logger

import json

class BasePublisher():
    def __init__(self,
                 exchange_name: str = "admin_exchange",
                 exchange_type: str = "fanout",
                 routing_key: Optional[str] = None
                 ):
        self.rabbitmq_management = RabbitMQManagement()
        self.rabbitmq_management.declare_exchange(exchange_name, exchange_type)
        if routing_key is not None and isinstance(routing_key, str):
            self.rabbitmq_management.routing_key = routing_key
        
    def get_exchange_name(self) -> str:
        exchange_name = self.rabbitmq_management.exchange_name
        if exchange_name is None:
            raise ValueError("The exchange has not been declared yet.")
        return exchange_name
    
    def get_routing_key(self) -> str:
        return self.rabbitmq_management.routing_key
    
    def publish(self, message: Union[str, bytes, dict, list, BaseModel]) -> None:
        if isinstance(message, str):
            message = message.encode()
        elif isinstance(message, (dict, list)):
            message = json.dumps(message).encode()
        elif isinstance(message, BaseModel):
            message = message.model_dump_json().encode()
        elif not isinstance(message, bytes):
            logger.error(f"Invalid message type: {type(message).__name__}. Expected str, bytes, dict, list, or Pydantic BaseModel.")
            raise TypeError("Message must be a string, bytes, a JSON-serializable object, or a Pydantic BaseModel instance")
        
        logger.info(f"Publishing message: {message} to the exchange: {self.get_exchange_name()} with routing key: {self.get_routing_key()}")
        self.rabbitmq_management.publish_message(message)
        logger.info("Message published successfully.")
    
    
    def close_connection(self) -> None:
        logger.info(f"Closing connection to the exchange: {self.get_exchange_name()}")
        self.rabbitmq_management.connection.close()
        logger.info("Connection closed successfully.")
