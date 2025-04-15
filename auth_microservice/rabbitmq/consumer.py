from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
import logging
import time
from pika.exceptions import AMQPConnectionError

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class TrialConsumer:
    def __init__(self, exchange_name: str = "admin_exchange", queue_name: str = "trial_queue_auth", host: str = "rabbitmq", port: int = 5672):
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.host = host
        self.port = port
        self.credentials = PlainCredentials("guest", "guest")
        self.connection = None
        self.channel = None

        # Retry mechanism for RabbitMQ connection
        for attempt in range(5):  # Retry up to 5 times
            try:
                logger.info(f"Attempting to connect to RabbitMQ (attempt {attempt + 1})...")
                self.connection = BlockingConnection(ConnectionParameters(host=self.host, port=self.port, credentials=self.credentials))
                self.channel: BlockingChannel = self.connection.channel()
                break
            except AMQPConnectionError as e:
                logger.error(f"Connection failed: {e}. Retrying in 5 seconds...")
                time.sleep(5)
        else:
            raise AMQPConnectionError("Failed to connect to RabbitMQ after 5 attempts.")

        # Declare exchange and queue
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type="fanout")
        self.channel.queue_declare(queue=self.queue_name)
        self.channel.queue_bind(exchange=self.exchange_name, queue=self.queue_name)
        logger.info(f"Connected to RabbitMQ. Declared exchange: {self.exchange_name}, queue: {self.queue_name}")

    def on_message(self, channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
        try:
            # Decode the message and log it
            message: str = body.decode('utf-8')
            logger.info(f"The queue: {self.queue_name} received message: {message}")
            channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logger.error(f"Unexpected error while processing message: {e}")
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def start(self):
        logger.info(f"Starting consumer on queue: {self.queue_name}")
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.on_message)
        self.channel.start_consuming()

    def stop(self):
        logger.info("Stopping consumer...")
        if self.channel.is_open:
            self.channel.stop_consuming()
        if self.connection.is_open:
            self.connection.close()
        logger.info("Consumer stopped and connection closed.")