# External Library imports
import json

# Internal Library imports
from src.logger_tool import logger
from src.message_broker_management.base_consumer import BaseConsumer, AbstractIncomingMessage
from src.util import handle_messages

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
                logger.info(f"Received message with routing key: {message.routing_key}")
                # Decode the message and log it
                message_body: str = message.body.decode("utf-8")
                # Parse the message body as JSON
                message_data = json.loads(message_body)
                # Handle the message based on the routing key
                handle_messages.handle_message(self.database, message_data, message.routing_key)
                await message.ack()
                logger.info(f"Message processed successfully: {message_body}")
            except Exception as e:
                await message.nack(requeue=True)
                logger.error(f"Failed to process message: {message_body}")




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