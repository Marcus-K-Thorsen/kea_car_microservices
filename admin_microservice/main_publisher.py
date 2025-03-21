# import os
# from dotenv import load_dotenv
# import pika
from pika import BlockingConnection, ConnectionParameters
from pika.frame import Method
from pika.exceptions import ChannelClosed
from pika.adapters.blocking_connection import BlockingChannel
from pydantic import BaseModel
from typing import Callable, Union, Literal, Optional, Dict, List, Any
from abc import ABC, abstractmethod

import json

# load_dotenv()

class RabbitMQManagement():
    def __init__(self) -> None:
        # host: str = os.getenv('RABBITMQ_HOST', 'localhost')
        host: str = 'localhost'
        connection_params: ConnectionParameters = ConnectionParameters(host=host)
        # Can you add more connection parameters here, with default values and some descriptive comments?
        
        self.queue_name: Optional[str] = None
        self.exchange_name: Optional[str] = None
        self.routing_keys: List[str] = []
        self.routing_key: str = ''
        self.connection: BlockingConnection = BlockingConnection(connection_params)
        self.channel: BlockingChannel = self.connection.channel()
    
    def does_queue_exist(self, queue_name: str) -> bool:
        if not isinstance(queue_name, str):
            raise TypeError('Queue name must be a string')
        try:
            self.channel.queue_declare(queue=queue_name, passive=True)
            return True
        except ChannelClosed as e:
            if e.reply_code == 404:
                return False
            else:
                raise e
            
    def does_exchange_exist(self, exchange_name: str) -> bool:
        if not isinstance(exchange_name, str):
            raise TypeError('Exchange name must be a string')
        try:
            self.channel.exchange_declare(exchange=exchange_name, passive=True)
            return True
        except ChannelClosed as e:
            if e.reply_code == 404:
                return False
            else:
                raise e


    def declare_exchange(self, 
                         exchange_name: str, 
                         exchange_type: Literal['direct', 'fanout', 'topic', 'headers'] = 'direct',
                         durable: bool = False,
                         auto_delete: bool = False,
                         ) -> Method:
        """
        Declare an exchange on the RabbitMQ server.

        This method creates an exchange if it does not already exist, and if the exchange exists,
        verifies that it is of the correct and expected class.
        
        :param str exchange_name: The name of the exchange. The exchange name is used to route messages to the appropriate queues.
        :param str exchange_type: The type of the exchange. Defaults to 'direct' because it provides simple and predictable routing behavior. Must be one of 'direct', 'fanout', 'topic', or 'headers'.
        
                                  - 'direct': Routes messages to queues based on the exact match between the routing key and the queue binding key.
                                  
                                  - 'fanout': Routes messages to all queues bound to the exchange, ignoring the routing key.
                                  
                                  - 'topic': Routes messages to queues based on pattern matching between the routing key and the queue binding key.
                                  
                                  - 'headers': Routes messages based on message header attributes instead of the routing key.
                                  
        :param bool durable: If True, the exchange will survive server restarts. Defaults to False.
                             Durable exchanges are useful for ensuring that the exchange remains available even after a server restart.
        :param bool auto_delete: If True, the exchange will be deleted when all queues have finished using it. Defaults to False.
                                 Auto-delete exchanges are useful for temporary exchanges that should be removed when no longer needed.
        :returns: Method frame from the Exchange.Declare-ok response. This can be used to get information about the declared exchange.
        :rtype: pika.frame.Method
        """
        # Validate exchange name
        if not exchange_name:
            raise ValueError('Exchange name must be provided')
        if not isinstance(exchange_name, str):
            raise TypeError('Exchange name must be a string')

        # Validate exchange type
        if not isinstance(exchange_type, str):
            raise TypeError("Exchange type must be a string")
        if exchange_type not in ['direct', 'fanout', 'topic', 'headers']:
            raise ValueError("Exchange type must be one of 'direct', 'fanout', 'topic', or 'headers'")
        
        # Validate boolean parameters
        if not isinstance(durable, bool):
            raise TypeError('Durable must be a boolean')
        if not isinstance(auto_delete, bool):
            raise TypeError('Auto_delete must be a boolean')
        

        # Declare the exchange
        self.exchange_name: str = exchange_name
        
        return self.channel.exchange_declare(
            exchange_name, 
            exchange_type,
            False,
            durable,
            auto_delete
        )


    def declare_queue(self, 
                      queue_name: str = '',
                      durable: bool = False, 
                      exclusive: bool = False, 
                      auto_delete: bool = False
                      ) -> Method:
        """
        Declare a queue on the RabbitMQ server.

        This method creates a queue if it does not already exist.

        :param str queue_name: The name of the queue. Must be a non-empty string containing only letters, digits, hyphen, underscore, period, or colon.
                               The queue name is used to route messages to the appropriate queues.
        :param bool passive: If True, the server will reply with Declare-Ok if the queue already exists with the same name, and raise an error if not. Defaults to False.
                             This is useful for checking if a queue exists without modifying it.
        :param bool durable: If True, the queue will survive server restarts. Defaults to False.
                             Durable queues are useful for ensuring that the queue remains available even after a server restart.
        :param bool exclusive: If True, the queue will be used by only one connection and will be deleted when that connection closes. Defaults to False.
        :param bool auto_delete: If True, the queue will be deleted when all consumers have finished using it. Defaults to False.
                                 Auto-delete queues are useful for temporary queues that should be removed when no longer needed.
        :returns: Method frame from the Queue.Declare-ok response. This can be used to get information about the declared queue.
        :rtype: pika.frame.Method
        """
        # Validate queue name
        if not isinstance(queue_name, str):
            raise TypeError('Queue name must be a string')

        # Validate boolean parameters
        if not isinstance(durable, bool):
            raise TypeError('Durable must be a boolean')
        if not isinstance(exclusive, bool):
            raise TypeError('Exclusive must be a boolean')
        if not isinstance(auto_delete, bool):
            raise TypeError('Auto_delete must be a boolean')

        # Declare the queue
        result: Method = self.channel.queue_declare(
            queue_name,
            False,
            durable, 
            exclusive, 
            auto_delete
        )
        
        self.queue_name: str = result.method.queue
        return result


    def bind_queue_to_exchange(self,
                   routing_key: Union[str, List[str], None] = None
                   ) -> Method:
        """
        Bind a queue to an exchange with a routing key on the RabbitMQ server. The queue and exchange must have been declared before calling this function.

        This method binds a queue to an exchange so that messages sent to the exchange with a matching routing key
        are routed to the queue.
        
        :param str | list[str] routing_key: The routing key or a list of routing keys. Must be a non-empty string, a list of non-empty strings containing only valid characters or None.
                                            The routing key is used to route messages to the appropriate queues.
                                            If None, the queue will be bound to the exchange with an empty routing key.
        :returns: Method frame from the Queue.Bind-ok response.
        :rtype: pika.frame.Method
        """
        
        # Check if the queue exists
        if self.queue_name is None or not self.does_queue_exist(self.queue_name):
            raise ValueError('Queue does not exist. Please declare the queue before binding it.')
        
        # Check if the exchange exists
        if self.exchange_name is None or not self.does_exchange_exist(self.exchange_name):
            raise ValueError('Exchange does not exist. Please declare the exchange before binding the queue.')

        # Check if routing key is provided
        if routing_key is not None:
            # Validate routing key
            if isinstance(routing_key, str):
                self.routing_key = routing_key
                routing_keys = [routing_key]
            elif isinstance(routing_key, list) and routing_key.count > 0 and all(isinstance(key, str) for key in routing_key):
                self.routing_keys = routing_key
                routing_keys = routing_key
            else:
                raise TypeError('Routing key must be a string or a list of strings')

            if not all(key and all(char.isalpha() or char in '*.#' for char in key) for key in routing_keys):
                raise ValueError('Routing key must contain only letters, stars, or hash symbols')

            # Bind the queue to the exchange with the routing key(s)
            the_first_routing_key = routing_keys.pop(0)
            result: Method = self.channel.queue_bind(self.queue_name, self.exchange_name, the_first_routing_key)
            for key in routing_keys:
                result: Method = self.channel.queue_bind(self.queue_name, self.exchange_name, key)

            return result
        
        # Bind the queue to the exchange without a routing key
        return self.channel.queue_bind(self.queue_name, self.exchange_name)
    
    def publish_message(self, message: Union[str, bytes]) -> None:
        """
        Publish a message to the exchange on the RabbitMQ server. The exchange must have been declared before calling this function.

        This method sends a message to the exchange, which will route it to the appropriate queues based on the routing key.
        
        :param str | bytes message: The message to be published. Must be a non-empty string or bytes.
        """
        # Check if the exchange exists
        if self.exchange_name is None or not self.does_exchange_exist(self.exchange_name):
            raise ValueError('Exchange does not exist. Please declare the exchange before publishing a message.')
        
        # Validate message
        if not isinstance(message, (str, bytes)):
            raise TypeError('Message must be a string or bytes')
        
        # Publish the message to the exchange
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.routing_key,
            body=message
        )





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

class TrialPublisher(FanoutPublisher):
    def __init__(self):
        super().__init__('trial_admin_exchange')


class TrialItem(BaseModel):
    item_name: str

class Trial(BaseModel):
    name: str
    age: int
    trial_item: TrialItem

def main(item_name: str = "item"):
    trial_item = TrialItem(item_name=item_name)
    trial = Trial(name="admin", age=20, trial_item=trial_item)
    
    trial_publisher = TrialPublisher()
    trial_publisher.publish(trial)
    print("Main publisher is running")
    print("Publisher is running")
    trial_publisher.close_connection()
    print("Publisher is closed")


# To start the admin publisher to publish one message, run this script while in the root of the project directory:
# poetry run python -m admin_microservice.main_publisher
if __name__ == '__main__':
    main()