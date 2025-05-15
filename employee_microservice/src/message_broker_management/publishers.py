# Internal library imports
from src.message_broker_management.base_publisher import BasePublisher


class InsuranceCreatedPublisher(BasePublisher):
    def __init__(self):
        super().__init__(routing_key="insurance.created")
        

class InsuranceUpdatedPublisher(BasePublisher):
    def __init__(self):
        super().__init__(routing_key="insurance.updated")

        
insurance_created_publisher = InsuranceCreatedPublisher()
insurance_updated_publisher = InsuranceUpdatedPublisher()
