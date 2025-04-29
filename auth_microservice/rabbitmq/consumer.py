from aio_pika import ExchangeType, connect_robust
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel, AbstractRobustExchange, AbstractRobustQueue, AbstractIncomingMessage
from typing import Optional
import asyncio
import logging
import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class TrialConsumer:
    def __init__(
        self,
        exchange_name: str = "admin_exchange",
        queue_name: str = "trial_queue_auth",
    ):
        self.exchange_name = exchange_name
        self.exchange: Optional[AbstractRobustExchange] = None
        self.queue_name = queue_name
        self.queue: Optional[AbstractRobustQueue] = None
        self.connection: Optional[AbstractRobustConnection] = None
        self.channel: Optional[AbstractRobustChannel] = None

    async def connect(self):
        """Establish a connection to RabbitMQ."""
        retries = 5
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
                logger.error(f"Connection failed: {e}. Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
        else:
            raise ConnectionError(f"Failed to connect to RabbitMQ after {retries} attempts (total time: {total_time} seconds).")

        # Declare exchange and queue
        self.exhange = await self.channel.declare_exchange(self.exchange_name, ExchangeType.FANOUT)
        self.queue = await self.channel.declare_queue(self.queue_name, durable=True)
        await self.queue.bind(self.exchange_name)
        logger.info(
            f"Connected to RabbitMQ. Declared exchange: {self.exchange_name}, queue: {self.queue_name}"
        )

    async def on_message(self, message: AbstractIncomingMessage):
        """Handle incoming messages."""
        async with message.process():
            try:
                logger.info(f"This is The Routing Key: {message.routing_key}")
                # Decode the message and log it
                message_body: str = message.body.decode("utf-8")
                logger.info(f"This is The queue: {self.queue_name} received message: {message_body}")
            except Exception as e:
                logger.error(f"Unexpected error while processing message: {e}")

    async def start(self):
        """Start consuming messages."""
        if not self.connection or not self.channel:
            await self.connect()
        
        logger.info(f"Starting consumer on queue: {self.queue_name}")
        await self.queue.consume(self.on_message)

    async def stop(self):
        """Close the connection."""
        logger.info("Stopping consumer...")
        if self.connection is not None and isinstance(self.connection, AbstractRobustConnection):
            await self.connection.close()
            self.connection = None
        
        if self.channel is not None and isinstance(self.channel, AbstractRobustChannel):
            await self.channel.close()
            self.channel = None
        logger.info("Consumer stopped and connection closed.")