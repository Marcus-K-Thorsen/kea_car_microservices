from modules import FanoutPublisher

class MessagePublisher(FanoutPublisher):
    def __init__(self):
        super().__init__('message_exchange')