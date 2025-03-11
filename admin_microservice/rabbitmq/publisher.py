import pika
from pika.adapters.blocking_connection import BlockingConnection

class Publisher:
    def __init__(self, exchange_name: str, routing_key: str):
        self.exchange_name = exchange_name
        self.routing_key = routing_key
        self.exchange_type = 'fanout'
        self.connection = BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(self.exchange_name, self.exchange_type)

    def publish(self, message: str):
        self.channel.basic_publish(exchange=self.exchange_name, routing_key=self.routing_key, body=message)
        print(f" [x] Sent {message}")

    def close(self):
        self.connection.close()