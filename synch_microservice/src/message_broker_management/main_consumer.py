# External Library imports
import json

# Internal Library imports
from src.logger_tool import logger
from src.message_broker_management.base_consumer import BaseConsumer, AbstractIncomingMessage
from src.util import handle_message

class MainConsumer(BaseConsumer):
    def __init__(self):
        super().__init__(
            exchange_name="employee_exchange",
            queue_name="synch_microservice_queue"
        )

    async def on_message(self, message: AbstractIncomingMessage):
        """Handle incoming messages."""
        async with message.process(requeue=True, reject_on_redelivered=True):
            try:
                logger.info(f"Received message with routing key: {message.routing_key}")
                # Decode the message and log it
                message_body: str = message.body.decode("utf-8")
                logger.info(f"Received message to process: {message_body}")
                # Parse the message body as JSON
                message_data = json.loads(message_body)
                # Handle the message based on the routing key
                handle_message(self.get_database_connection(), message_data, message.routing_key)
                logger.info(f"Message processed successfully: {message_data}")
            except Exception as e:
                # Log the error
                logger.error(f"Error processing message: {e}")
                logger.warning(f"Will requeue the message: {message.body}")
                raise




def get_employee_exchange_consumer() -> MainConsumer:
    return MainConsumer()

async def start_consumer(consumer: MainConsumer) -> None:
    """Start the consumer."""
    if isinstance(consumer, MainConsumer):
        await consumer.start()

async def stop_consumer(consumer: MainConsumer) -> None:
    """Stop the consumer."""
    if isinstance(consumer, MainConsumer):
        await consumer.stop()