from aio_pika import ExchangeType, IncomingMessage, connect_robust
import asyncio
import logging
import os

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
        host: str = "rabbitmq",
        port: int = 5672,
    ):
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.host = host
        self.port = port
        self.connection = None
        self.channel = None

    async def connect(self):
        """Establish a connection to RabbitMQ."""
        for attempt in range(5):  # Retry up to 5 times
            try:
                logger.info(f"Attempting to connect to RabbitMQ (attempt {attempt + 1})...")
                self.connection = await connect_robust(
                    host=self.host,
                    port=self.port,
                    login=os.getenv("RABBITMQ_USERNAME", "guest"),
                    password=os.getenv("RABBITMQ_PASSWORD", "guest"),
                )
                self.channel = await self.connection.channel()
                break
            except Exception as e:
                logger.error(f"Connection failed: {e}. Retrying in 5 seconds...")
                await asyncio.sleep(5)
        else:
            raise ConnectionError("Failed to connect to RabbitMQ after 5 attempts.")

        # Declare exchange and queue
        await self.channel.declare_exchange(self.exchange_name, ExchangeType.FANOUT)
        queue = await self.channel.declare_queue(self.queue_name, durable=True)
        await queue.bind(self.exchange_name)
        logger.info(
            f"Connected to RabbitMQ. Declared exchange: {self.exchange_name}, queue: {self.queue_name}"
        )

    async def on_message(self, message: IncomingMessage):
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

        queue = await self.channel.declare_queue(self.queue_name, durable=True)
        logger.info(f"Starting consumer on queue: {self.queue_name}")
        await queue.consume(self.on_message)

    async def stop(self):
        """Close the connection."""
        logger.info("Stopping consumer...")
        if self.connection:
            await self.connection.close()
            self.connection = None
        logger.info("Consumer stopped and connection closed.")