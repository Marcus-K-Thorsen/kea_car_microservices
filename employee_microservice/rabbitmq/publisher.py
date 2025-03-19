from modules import FanoutPublisher

class MessagePublisher(FanoutPublisher):
    def __init__(self):
        super().__init__('trial_employee_exchange')