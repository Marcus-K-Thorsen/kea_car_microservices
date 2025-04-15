import sys
import os
from rabbitmq.consumer import TrialConsumer as Consumer

def main():
    print(' [*] Waiting for consumer. To exit press CTRL+C')
    from_admin_consumer = Consumer()
    from_admin_consumer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        from_admin_consumer.close_connection()
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)