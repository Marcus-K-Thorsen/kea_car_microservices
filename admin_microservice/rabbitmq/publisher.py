from modules import FanoutPublisher


class TrialPublisher(FanoutPublisher):
    def __init__(self):
        super().__init__('trial_admin_exchange')