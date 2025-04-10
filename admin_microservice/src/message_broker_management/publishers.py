from .base_publisher import BasePublisher


class EmployeeCreatedPublisher(BasePublisher):
    def __init__(self):
        super().__init__(routing_key="employee.created")
        

class EmployeeUpdatedPublisher(BasePublisher):
    def __init__(self):
        super().__init__(routing_key="employee.updated")


class EmployeeDeletedPublisher(BasePublisher):
    def __init__(self):
        super().__init__(routing_key="employee.deleted")


class TrialPublisher(BasePublisher):
    def __init__(self):
        super().__init__(routing_key="trial")