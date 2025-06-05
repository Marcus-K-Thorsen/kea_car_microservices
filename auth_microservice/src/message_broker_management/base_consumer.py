# External Library imports
import os
import asyncio
from typing import Optional
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from aio_pika import ExchangeType, connect_robust

from aio_pika.abc import (
    AbstractRobustConnection,
    AbstractIncomingMessage,
    AbstractRobustExchange, 
    AbstractRobustChannel, 
    AbstractRobustQueue
)

# Internal Library imports
from src.logger_tool import logger
from src.database_management import get_mongodb, Database


load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")


class BaseConsumer(ABC):
    def __init__(
        self,
        exchange_name: str,
        queue_name: str,
    ):
        self.exchange_name = exchange_name
        self.exchange: Optional[AbstractRobustExchange] = None
        self.queue_name = queue_name
        self.queue: Optional[AbstractRobustQueue] = None
        self.connection: Optional[AbstractRobustConnection] = None
        self.channel: Optional[AbstractRobustChannel] = None
        with get_mongodb(as_administrator=True) as database:
            if not isinstance(database, Database):
                raise TypeError(f"Database connection is not of type Database, but the type: {type(database).__name__}.")
            self.database: Database = database

    async def connect(self):
        """Establish a connection to RabbitMQ."""
        retries = 15
        delay = 5
        total_time = 0
        for attempt in range(retries):
            try:
                logger.info(f"Attempting to connect to RabbitMQ (attempt {attempt + 1}/{retries})...")
                self.connection = await connect_robust(
                    host=RABBITMQ_HOST,
                    port=RABBITMQ_PORT,
                    login=RABBITMQ_USERNAME,
                    password=RABBITMQ_PASSWORD,
                )
                self.channel = await self.connection.channel()
                break
            except Exception as e:
                total_time += delay
                logger.warning(f"Connection failed: {e}. Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
        else:
            raise ConnectionError(f"Failed to connect to RabbitMQ after {retries} attempts (total time: {total_time} seconds).")

        # Declare exchange and queue
        self.exhange = await self.channel.declare_exchange(self.exchange_name, ExchangeType.FANOUT, durable=True)
        self.queue = await self.channel.declare_queue(self.queue_name, durable=True)
        await self.queue.bind(self.exchange_name)
        logger.info(
            f"Connected to RabbitMQ. Declared exchange: {self.exchange_name}, queue: {self.queue_name}"
        )
        
    def is_database_connected(self) -> bool:
        """Check if the database connection is established."""
        if not isinstance(self.database, Database):
            logger.warning("Database connection is not established.")
            return False
        try:
            # Check if the database client is connected by accessing its address
            if self.database.client.address is not None:
                return True
        except Exception as e:
            logger.warning(f"Database connection check failed and therefor is not connected: {e}")
            return False

        return False
    
    def close_database_connection(self):
        """Close the database connection."""
        self.database.client.close()
        self.database = None
        logger.info("Database connection closed.")
        
    def create_database_connection(self):
        """Create a new database connection."""
        with get_mongodb(as_administrator=True) as database:
            if not isinstance(database, Database):
                raise TypeError(f"Database connection is not of type Database, but the type: {type(database).__name__}.")
            self.database = database
            
    def get_database_connection(self) -> Database:
        """Get the database connection."""
        if not self.is_database_connected():
            logger.warning("Database connection is not established. Creating a new database connection.")
            self.create_database_connection()
        if not self.is_database_connected():
            raise ConnectionError("Failed to establish a database connection.")
        return self.database

    @abstractmethod
    async def on_message(self, message: AbstractIncomingMessage):
        """Handle incoming messages."""
        pass

    async def start(self):
        """Start consuming messages."""
        if not self.connection or not self.channel or not self.queue or not self.exchange:
            logger.info("Connecting to RabbitMQ...")
            await self.connect()
        
        logger.info(f"Starting consumer on queue: {self.queue_name}...")
        await self.queue.consume(self.on_message)
        
        if not self.is_database_connected():
            self.create_database_connection()

    async def stop(self):
        """Close the connection."""
        logger.info(f"Stopping consumer on queue: {self.queue_name}...")
        if self.connection is not None and isinstance(self.connection, AbstractRobustConnection):
            await self.connection.close()
            self.connection = None
        
        if self.channel is not None and isinstance(self.channel, AbstractRobustChannel):
            await self.channel.close()
            self.channel = None
        if self.is_database_connected():
            self.close_database_connection()
        
        logger.info("Consumer stopped and connection closed.")