# External Library imports
import os
import time
from datetime import datetime
from pika.frame import Method
from dotenv import load_dotenv
from pika.exceptions import ChannelClosed, AMQPConnectionError
from typing import Union, Literal, Optional, List
from pika.adapters.blocking_connection import BlockingChannel
from pika import BlockingConnection, ConnectionParameters, PlainCredentials

# Internal library imports
from src.logger_tool import logger


load_dotenv()

HOST: str = os.getenv('RABBITMQ_HOST', 'rabbitmq')
try:
    PORT: int = int(os.getenv('RABBITMQ_PORT', 5672))
except ValueError:
    raise ValueError('RABBITMQ_PORT must be an integer')
USERNAME: str = os.getenv('RABBITMQ_USERNAME', 'guest')
PASSWORD: str = os.getenv('RABBITMQ_PASSWORD', 'guest')
CREDENTIALS = PlainCredentials(USERNAME, PASSWORD)


class RabbitMQManagement():
    def __init__(self) -> None:
        connection_params = ConnectionParameters(
            host=HOST,
            port=PORT,
            credentials=CREDENTIALS,
            heartbeat=0
            )
        self.connection_params: ConnectionParameters = connection_params
        
        self.queue_name: Optional[str] = None
        self.exchange_name: Optional[str] = None
        self.routing_keys: List[str] = []
        self.routing_key: str = ''
        self.connect()
    
    def does_queue_exist(self, queue_name: str) -> bool:
        if not isinstance(queue_name, str):
            logger.error(f'Queue name must be a string, not type: {type(queue_name).__name__}')
            raise TypeError('Queue name must be a string')
        try:
            self.channel.queue_declare(queue=queue_name, passive=True)
            return True
        except ChannelClosed as e:
            if e.reply_code == 404:
                return False
            else:
                logger.error(f'Error checking if queue: {queue_name} exists: {e}')
                raise e
            
    def does_exchange_exist(self, exchange_name: str) -> bool:
        if not isinstance(exchange_name, str):
            logger.error(f'Exchange name must be a string, not type: {type(exchange_name).__name__}')
            raise TypeError('Exchange name must be a string')
        try:
            self.channel.exchange_declare(exchange=exchange_name, passive=True)
            return True
        except ChannelClosed as e:
            if e.reply_code == 404:
                return False
            else:
                logger.error(f'Error checking if exchange: {exchange_name} exists: {e}')
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
        logger.info(f'Declaring exchange: {exchange_name} of type: {exchange_type} with durable: {durable} and auto_delete: {auto_delete}')
        # Validate exchange name
        if not exchange_name:
            logger.error('Exchange name must be provided')
            raise ValueError('Exchange name must be provided')
        if not isinstance(exchange_name, str):
            logger.error(f'Exchange name must be a string, not type: {type(exchange_name).__name__}')
            raise TypeError('Exchange name must be a string')

        # Validate exchange type
        if not isinstance(exchange_type, str):
            logger.error(f'Exchange type must be a string, not type: {type(exchange_type).__name__}')
            raise TypeError("Exchange type must be a string")
        if exchange_type not in ['direct', 'fanout', 'topic', 'headers']:
            logger.error(f'Exchange type must be one of "direct", "fanout", "topic", or "headers", not: {exchange_type}')
            raise ValueError("Exchange type must be one of 'direct', 'fanout', 'topic', or 'headers'")
        
        # Validate boolean parameters
        if not isinstance(durable, bool):
            logger.error(f'Durable must be a boolean, not type: {type(durable).__name__}')
            raise TypeError('Durable must be a boolean')
        if not isinstance(auto_delete, bool):
            logger.error(f'Auto_delete must be a boolean, not type: {type(auto_delete).__name__}')
            raise TypeError('Auto_delete must be a boolean')
        

        # Declare the exchange
        self.exchange_name: str = exchange_name
        
        logger.info(f'Successfully declared exchange: {exchange_name}.')
        
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
        logger.info(f'Declaring queue: {queue_name} with durable: {durable}, exclusive: {exclusive}, and auto_delete: {auto_delete}')
        # Validate queue name
        if not isinstance(queue_name, str):
            logger.error(f'Queue name must be a string, not type: {type(queue_name).__name__}')
            raise TypeError('Queue name must be a string')

        # Validate boolean parameters
        if not isinstance(durable, bool):
            logger.error(f'Durable must be a boolean, not type: {type(durable).__name__}')
            raise TypeError('Durable must be a boolean')
        if not isinstance(exclusive, bool):
            logger.error(f'Exclusive must be a boolean, not type: {type(exclusive).__name__}')
            raise TypeError('Exclusive must be a boolean')
        if not isinstance(auto_delete, bool):
            logger.error(f'Auto_delete must be a boolean, not type: {type(auto_delete).__name__}')
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
        logger.info(f'Successfully declared queue: {self.queue_name}.')
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
        logger.info(f'Binding queue: {self.queue_name} to exchange: {self.exchange_name} with routing key: {routing_key}')
        # Check if the queue exists
        if self.queue_name is None or not self.does_queue_exist(self.queue_name):
            logger.error('Queue does not exist. Please declare the queue before binding it.')
            raise ValueError('Queue does not exist. Please declare the queue before binding it.')
        
        # Check if the exchange exists
        if self.exchange_name is None or not self.does_exchange_exist(self.exchange_name):
            logger.error('Exchange does not exist. Please declare the exchange before binding the queue.')
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
                logger.error(f'Routing key must be a string or a list of strings, not type: {type(routing_key).__name__}')
                raise TypeError('Routing key must be a string or a list of strings')

            if not all(key and all(char.isalpha() or char in '*.#' for char in key) for key in routing_keys):
                logger.error('Routing key must contain only letters, stars, or hash symbols')
                raise ValueError('Routing key must contain only letters, stars, or hash symbols')

            # Bind the queue to the exchange with the routing key(s)
            the_first_routing_key = routing_keys.pop(0)
            result: Method = self.channel.queue_bind(self.queue_name, self.exchange_name, the_first_routing_key)
            for key in routing_keys:
                result: Method = self.channel.queue_bind(self.queue_name, self.exchange_name, key)
            logger.info(f'Successfully bound queue: {self.queue_name} to exchange: {self.exchange_name} with routing keys: {routing_keys}.')
            return result
        
        # Bind the queue to the exchange without a routing key
        logger.info(f'Binding queue: {self.queue_name} to exchange: {self.exchange_name} without a routing key.')
        return self.channel.queue_bind(self.queue_name, self.exchange_name)
    
    def connect(self):
        """Reconnect to RabbitMQ and reopen the channel with retry logic."""
        max_retries = 15
        delay = 5  # seconds
        attempt = 0

        start_time = datetime.now()
        while attempt < max_retries:
            attempt += 1
            try:
                logger.info(f"Attempt {attempt} to connect to RabbitMQ at {self.connection_params.host}:{self.connection_params.port}...")
                self.connection = BlockingConnection(self.connection_params)
                self.channel = self.connection.channel()
                elapsed = (datetime.now() - start_time).total_seconds()
                logger.info(f"Reconnected to RabbitMQ successfully on attempt {attempt} after {elapsed:.2f} seconds.")
                return
            except Exception as e:
                logger.warning(f"Attempt {attempt} failed: {e}")
                if attempt == max_retries:
                    elapsed = (datetime.now() - start_time).total_seconds()
                    logger.error(f"Failed to reconnect to RabbitMQ after {max_retries} attempts and {elapsed:.2f} seconds.")
                    raise
                time.sleep(delay)
    
    def publish_message(self, message: Union[str, bytes]) -> None:
        """
        Publish a message to the exchange on the RabbitMQ server. The exchange must have been declared before calling this function.

        This method sends a message to the exchange, which will route it to the appropriate queues based on the routing key.
        
        :param str | bytes message: The message to be published. Must be a non-empty string or bytes.
        """
        try:
            # Check if the channel is open
            if self.channel.is_closed:
                logger.warning("Channel is closed. Attempting to reconnect...")
                self.connect()
                
            # Check if the exchange exists
            logger.info(f'Publishing message: {message} to exchange: {self.exchange_name} with routing key: {self.routing_key}')
            if self.exchange_name is None or not self.does_exchange_exist(self.exchange_name):
                logger.error('Exchange does not exist. Please declare the exchange before publishing a message.')
                raise ValueError('Exchange does not exist. Please declare the exchange before publishing a message.')
        
            # Validate message
            if not isinstance(message, (str, bytes)):
                logger.error(f'Message must be a string or bytes, not type: {type(message).__name__}')
                raise TypeError('Message must be a string or bytes')
        
            # Publish the message to the exchange
            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key=self.routing_key,
                body=message
            )
            logger.info(f'Successfully published message: {message} to exchange: {self.exchange_name} with routing key: {self.routing_key}.')
        except AMQPConnectionError as e:
            logger.error(f'Connection error while publishing message: {e}')
            self.connect()
            self.publish_message(message)
        except Exception as e:
            logger.error(f'Error publishing message: {e}')
            raise e

