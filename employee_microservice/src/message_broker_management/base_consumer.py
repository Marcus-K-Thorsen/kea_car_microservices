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
from src.database_management import get_mysqldb, Session


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
        with get_mysqldb(as_administrator=True) as session:
            if not isinstance(session, Session):
                raise TypeError(f"Session connection is not of type Session, but the type: {type(session).__name__}.")
            self.session: Session = session

    async def connect(self):
        """Establish a connection to RabbitMQ."""
        retries = 15
        delay = 6
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
        self.exchange = await self.channel.declare_exchange(self.exchange_name, ExchangeType.FANOUT, durable=True)
        self.queue = await self.channel.declare_queue(self.queue_name, durable=True)
        await self.queue.bind(self.exchange_name)
        logger.info(
            f"Connected to RabbitMQ. Declared exchange: {self.exchange_name}, queue: {self.queue_name}"
        )
        
    def is_session_connected(self) -> bool:
        """Check if the session connection is established."""
        if not isinstance(self.session, Session):
            logger.warning("Session connection is not established.")
            return False
        return self.session.is_active and self.session.bind is not None
    
    def close_session_connection(self):
        """Close the session connection."""
        self.session.close()
        self.session = None
        logger.info("Session connection closed.")
        
    def create_session_connection(self):
        """Create a new session connection."""
        with get_mysqldb(as_administrator=True) as session:
            if not isinstance(session, Session):
                raise TypeError(f"Session connection is not of type Session, but the type: {type(session).__name__}.")
            self.session = session
    
    def get_session_connection(self) -> Session:
        """Get the session connection."""
        if not self.is_session_connected():
            logger.warning("Session connection is not established. Creating a new session connection.")
            self.create_session_connection()
        if not self.is_session_connected():
            raise ConnectionError("Session connection is not established.")
        return self.session

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
        
        if not self.is_session_connected():
            self.create_session_connection()

    async def stop(self):
        """Close the connection."""
        logger.info(f"Stopping consumer on queue: {self.queue_name}...")
        if self.connection is not None and isinstance(self.connection, AbstractRobustConnection):
            await self.connection.close()
            self.connection = None
        
        if self.channel is not None and isinstance(self.channel, AbstractRobustChannel):
            await self.channel.close()
            self.channel = None
        if self.is_session_connected():
            self.close_session_connection()
        
        logger.info("Consumer stopped and connection closed.")