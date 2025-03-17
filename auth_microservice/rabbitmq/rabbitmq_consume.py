import os
from dotenv import load_dotenv
import pika
from pika import BlockingConnection, ConnectionParameters
from pika.frame import Method
from pika.exceptions import ChannelClosed
from pika.spec import Basic, BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
from typing import Callable, Union, Literal, Optional, Dict, List, Any
from abc import ABC, abstractmethod

load_dotenv()

class RabbitMQManagement(ABC):
    def __init__(self, queue_name: str = '') -> None:
        host: str = os.getenv('RABBITMQ_HOST', 'localhost')
        connection_params: ConnectionParameters = ConnectionParameters(host=host)
        
        self.queue_name = queue_name
        self.connection: BlockingConnection = BlockingConnection(connection_params)
        self.channel: BlockingChannel = self.connection.channel()
    
    def does_queue_exist(self, queue_name: str) -> bool:
        try:
            self.channel.queue_declare(queue=queue_name, passive=True)
            return True
        except ChannelClosed as e:
            if e.reply_code == 404:
                return False
            else:
                raise e
            
    def does_exchange_exist(self, exchange_name: str) -> bool:
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
        
        :param str exchange_name: The name of the exchange. Must be a non-empty string containing only letters, digits, hyphen, underscore, period, or colon.
                                  The exchange name is used to route messages to the appropriate queues.
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
        :raises ValueError: If the exchange name contains invalid characters.
        """
        # Validate exchange name
        if not exchange_name:
            raise ValueError('Exchange name must be provided')
        if not isinstance(exchange_name, str):
            raise TypeError('Exchange name must be a string')
        if not all(char.isalnum() or char in '-_.:' for char in exchange_name):
            raise ValueError('Exchange name must contain only letters, digits, hyphen, underscore, period, or colon')

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
        :raises ValueError: If the queue name contains invalid characters.
        """
        # Validate queue name
        if not isinstance(queue_name, str):
            raise TypeError('Queue name must be a string')
        #if not all(char.isalnum() or char in '-_.:' for char in queue_name):
        #    raise ValueError('Queue name must contain only letters, digits, hyphen, underscore, period, or colon')

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
        
        self.queue_name = result.method.queue
        return result


    def bind_queue(self, 
                   queue_name: str, 
                   exchange_name: str, 
                   routing_key: Union[str, List[str]]
                   ) -> Method:
        """
        Bind a queue to an exchange with a routing key on the RabbitMQ server.

        This method binds a queue to an exchange so that messages sent to the exchange with a matching routing key
        are routed to the queue.

        :param str queue_name: The name of the queue. Must be a non-empty string containing only letters, digits, hyphen, underscore, period, or colon.
                               The queue name must refer to a queue that has been declared.
        :param str exchange_name: The name of the exchange. Must be a non-empty string containing only letters, digits, hyphen, underscore, period, or colon.
                                  The exchange name must refer to an exchange that has been declared.
        :param str | list[str] routing_key: The routing key or a list of routing keys. Must be a non-empty string or a list of non-empty strings containing only valid characters.
        :returns: Method frame from the Queue.Bind-ok response.
        :rtype: pika.frame.Method
        :raises ValueError: If the queue name, exchange name, or routing key contains invalid characters or is not declared.
        :raises TypeError: If the queue name, exchange name, or routing key is not of the correct type.
        """
        # Validate queue name
        if not isinstance(queue_name, str):
            raise TypeError('Queue name must be a string')
        #if not all(char.isalpha() or char in '-_.:' for char in queue_name):
        #    raise ValueError('Queue name must contain only letters, hyphen, underscore, period, or colon')
        
        # Check if the queue exists
        if not self.does_queue_exist(queue_name):
            raise ValueError(f'Queue with name: {queue_name} does not exist.')

        # Validate exchange name
        if not isinstance(exchange_name, str):
            raise TypeError('Exchange name must be a string')
        if not all(char.isalpha() or char in '-_.:' for char in exchange_name):
            raise ValueError(f'Exchange name: {exchange_name} must contain only letters, hyphen, underscore, period, or colon')
        
        # Check if the exchange exists
        if not self.does_exchange_exist(exchange_name):
            raise ValueError(f'Exchange with name: {exchange_name} does not exist.')

        # Validate routing key
        if isinstance(routing_key, str):
            routing_keys = [routing_key]
        elif isinstance(routing_key, list) and routing_key.count > 0 and all(isinstance(key, str) for key in routing_key):
            routing_keys = routing_key
        else:
            raise TypeError('Routing key must be a string or a list of strings')

        if not all(key and all(char.isalpha() or char in '*.#' for char in key) for key in routing_keys):
            raise ValueError('Routing key must contain only letters, stars, or hash symbols')

        # Bind the queue to the exchange with the routing key(s)
        the_first_routing_key = routing_keys.pop(0)
        result = self.channel.queue_bind(queue_name, exchange_name, the_first_routing_key)
        for key in routing_keys:
            result = self.channel.queue_bind(queue_name, exchange_name, key)

        return result


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
        self.channel.basic_consume(self.queue_name, on_message_callback=self.on_message, auto_ack=auto_acknowledge)
        print(f"Starting to consume from queue: {self.queue_name}")
        self.channel.start_consuming()
        
    def consume_message(self, auto_acknowledge: bool = False) -> Any:
        return self.channel.basic_consume(self.queue_name, on_message_callback=self.on_message, auto_ack=auto_acknowledge)
        

    def close_connection(self) -> None:
        self.connection.close()
        
        
        

class Consumer(RabbitMQManagement):
    
    def __init__(self, queue_name = ''):
        super().__init__(queue_name)
        self.exchange_name = 'admin_exchange'
        self.exchange_type = 'fanout'
        self.routing_key = 'employee.message'
        self.setup()
        
    def setup(self) -> None:
        self.declare_exchange(self.exchange_name, self.exchange_type)
        self.declare_queue(self.queue_name)
        self.bind_queue(self.queue_name, self.exchange_name, self.routing_key)
    
            
    def on_message(self, 
                   ch: BlockingChannel, 
                   method: Basic.Deliver, 
                   properties: BasicProperties, 
                   body: bytes
                   ) -> None:
        print(f"Received message: {body.decode()}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"Acknowledged message: {body}")