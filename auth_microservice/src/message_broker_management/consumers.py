from typing import List, Union
from pydantic import BaseModel
import json

from .base_consumer import BaseConsumer, BlockingChannel, Basic, BasicProperties

# Trial stuff, delete later

class TrialMessage(BaseModel):
    message: str

class TrialConsumer(BaseConsumer):
    def __init__(self, 
                 queue_name: str
                 ):
        super().__init__()
        self.initial_setup(
            exchange_name='admin_exchange', 
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
    
    def on_message(self, 
                   ch: BlockingChannel, 
                   method: Basic.Deliver, 
                   properties: BasicProperties, 
                   body: bytes
                   ) -> None:
        message: str = body.decode('utf-8')
        print(f"The queue: {self.get_queue_name} received message: {message}")
        trial_dict: dict = json.loads(message)
        trial_message = TrialMessage(message=trial_dict.get('message'))
        print(f"Parsed Trial object: {trial_message}")
        ch.basic_ack(delivery_tag=method.delivery_tag)