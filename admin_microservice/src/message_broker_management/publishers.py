# Internal library imports
from src.message_broker_management.base_publisher import BasePublisher


class EmployeeCreatedPublisher(BasePublisher):
    def __init__(self):
        super().__init__(routing_key="employee.created")
        

class EmployeeUpdatedPublisher(BasePublisher):
    def __init__(self):
        super().__init__(routing_key="employee.updated")


class EmployeeDeletedPublisher(BasePublisher):
    def __init__(self):
        super().__init__(routing_key="employee.deleted")


class EmployeeUndeletedPublisher(BasePublisher):
    def __init__(self):
        super().__init__(routing_key="employee.undeleted")
        

        
employee_created_publisher = EmployeeCreatedPublisher()
employee_updated_publisher = EmployeeUpdatedPublisher()
employee_deleted_publisher = EmployeeDeletedPublisher()
employee_undeleted_publisher = EmployeeUndeletedPublisher()
