import sys
import os
from rabbitmq.consumer import Consumer


def main():
    print(' [*] Waiting for consumer. To exit press CTRL+C')
    from_admin_consumer = Consumer()
    message = from_admin_consumer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        message.close_connection()
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == '__main__':
    main()
    