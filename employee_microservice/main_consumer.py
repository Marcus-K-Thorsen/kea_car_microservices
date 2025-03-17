import sys
import os
from employee_microservice.rabbitmq.consumer_trial import TrialConsumer

# To start the consumer, run this script while in the root of the project directory:
# poetry run python -m employee_microservice.main_consumer
def main():
    print(' [*] Waiting for consumer. To exit press CTRL+C')
    trial_consumer = TrialConsumer()
    trial_consumer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        trial_consumer.close_connection()
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == '__main__':
    main()
    