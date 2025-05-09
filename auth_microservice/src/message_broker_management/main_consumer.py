# External Library imports
import json

# Internal Library imports
from src.logger_tool import logger
from .base_consumer import BaseConsumer, AbstractIncomingMessage

class MainConsumer(BaseConsumer):
    def __init__(self):
        super().__init__(
            exchange_name="admin_exchange",
            queue_name="auth_microservice_queue",
        )

    async def on_message(self, message: AbstractIncomingMessage):
        """Handle incoming messages."""
        async with message.process():
            try:
                logger.info(f"This is The Routing Key: {message.routing_key}!")
                # Decode the message and log it
                message_body: str = message.body.decode("utf-8")
                logger.info(f"This is The queue: {self.queue_name} received message: {message_body}")
                # Parse the message body as JSON
                message_data = json.loads(message_body)
                logger.info(f"Received message data: {message_data}")
            except Exception as e:
                logger.error(f"Unexpected error while processing message: {e}")




def get_admin_exchange_consumer() -> MainConsumer:
    return MainConsumer()

async def start_consumer(consumer: MainConsumer) -> None:
    """Start the consumer."""
    if isinstance(consumer, MainConsumer):
        await consumer.start()

async def stop_consumer(consumer: MainConsumer) -> None:
    """Stop the consumer."""
    if isinstance(consumer, MainConsumer):
        await consumer.stop()