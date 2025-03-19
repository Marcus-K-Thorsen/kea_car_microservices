import sys
import os
from .rabbitmq.consumer import TrialConsumer as Consumer


def main():
    print(' [*] Waiting for consumer. To exit press CTRL+C')
    from_employee_consumer = Consumer()
    from_employee_consumer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        from_employee_consumer.close_connection()
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

# To start the synchronizer microservice consumer, run this script while in the root of the project directory:
# poetry run python -m synch_microservice.main_consumer
if __name__ == '__main__':
    main()
    