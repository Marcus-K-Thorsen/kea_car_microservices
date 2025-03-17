from typing import Union, Optional, Any
from pydantic import BaseModel
import json

from .rabbitmq_management import RabbitMQManagement

class BasePublisher():
    def __init__(self,
                 exchange_name: str,
                 exchange_type: str,
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
            raise TypeError("Message must be a string, bytes, a JSON-serializable object, or a Pydantic BaseModel instance")
        
        self.rabbitmq_management.publish_message(message)
        print(f" [x] Sent {message} to the exchange: {self.get_exchange_name()} with routing key: {self.get_routing_key()}")
    
    
    def close_connection(self) -> None:
        print(f"Closing connection to the exchange: {self.get_exchange_name()}")
        self.rabbitmq_management.connection.close()    


class FanoutPublisher(BasePublisher):
    def __init__(self, exchange_name: str):
        super().__init__(exchange_name, 'fanout')

