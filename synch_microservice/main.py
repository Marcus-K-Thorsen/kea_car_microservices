# External Library imports
import asyncio
import signal

# Internal Library imports
from src.message_broker_management import get_employee_exchange_consumer, start_consumer, stop_consumer
from src.logger_tool import logger

shutdown_event = asyncio.Event()

def _signal_handler():
    logger.info("Received shutdown signal.")
    shutdown_event.set()

async def main():
    consumer = get_employee_exchange_consumer()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, _signal_handler)

    try:
        logger.info("Starting RabbitMQ consumer...")
        await start_consumer(consumer)
        logger.info("RabbitMQ consumer started. Waiting for shutdown signal.")
        await shutdown_event.wait()
    finally:
        logger.info("Stopping RabbitMQ consumer...")
        await stop_consumer(consumer)
        logger.info("Consumer stopped. Exiting.")

if __name__ == "__main__":
    asyncio.run(main())