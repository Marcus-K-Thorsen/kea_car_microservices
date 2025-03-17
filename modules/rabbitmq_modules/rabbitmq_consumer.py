from abc import ABC, abstractmethod
from typing import Union, List
from pika.spec import Basic, BasicProperties
from pika.adapters.blocking_connection import BlockingChannel

from .rabbitmq_management import RabbitMQManagement

class BaseConsumer(ABC):
    def __init__(self):
        self.rabbitmq_management = RabbitMQManagement()
        
    def get_queue_name(self) -> str:
        queue_name = self.rabbitmq_management.queue_name
        if queue_name is None:
            raise ValueError("The queue has not been declared yet.")
        return queue_name
    
    def get_exchange_name(self) -> str:
        exchange_name = self.rabbitmq_management.exchange_name
        if exchange_name is None:
            raise ValueError("The exchange has not been declared yet.")
        return exchange_name
    
    def get_routing_keys(self) -> List[str]:
        return self.rabbitmq_management.routing_keys
    
    @abstractmethod
    def initial_setup(self,
                      exchange_name: str, 
                      exchange_type: str,
                      queue_name: str = '',
                      routing_keys: Union[List[str], str, None] = None
                      ) -> None:
        """
        Abstract method to setup the exchange, queue and bind the queue to the exchange. Must be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def on_message(self, 
                   ch: BlockingChannel, 
                   method: Basic.Deliver, 
                   properties: BasicProperties, 
                   body: bytes
                   ) -> None:
        """
        Abstract method to handle incoming messages. Must be implemented by subclasses.
        """
        pass
    
    def start(self, auto_acknowledge: bool = False) -> None:
        queue_name = self.get_queue_name()
        self.rabbitmq_management.channel.basic_consume(
            queue_name, 
            on_message_callback=self.on_message, 
            auto_ack=auto_acknowledge
            )
        
        print(f"Starting to consume from queue: {queue_name}")
        self.rabbitmq_management.channel.start_consuming()
    
    def close_connection(self) -> None:
        self.rabbitmq_management.connection.close()
    
    
    

class FanoutConsumer(BaseConsumer):
    def __init__(self, 
                 exchange_name: str, 
                 queue_name: str
                 ):
        super().__init__()
        self.initial_setup(
            exchange_name=exchange_name, 
            exchange_type='fanout',
            queue_name=queue_name
            )
        
        
    def initial_setup(self, 
                      exchange_name: str, 
                      exchange_type: str,
                      queue_name: str = '',
                      routing_keys: Union[List[str], str, None] = None
                      ) -> None:
        self.rabbitmq_management.declare_exchange(exchange_name, exchange_type)
        self.rabbitmq_management.declare_queue(queue_name)
        self.rabbitmq_management.bind_queue_to_exchange(routing_keys)
    
