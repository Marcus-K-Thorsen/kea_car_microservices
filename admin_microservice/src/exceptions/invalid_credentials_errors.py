# External Library imports
from typing import Union, List

# Internal Library imports
from src.resources import RoleEnum
from src.entities import EmployeeEntity

class IncorrectCredentialError(Exception):
    """Base class for exceptions related to incorrect credentials"""
    pass

class IncorrectEmailError(IncorrectCredentialError):
    """Exception raised for incorrect email"""

    def __init__(self, email: str):
        self.message = f"The email '{email}' is incorrect."
        super().__init__(self.message)  # Call the base class constructor

    def __str__(self):
        return f"{self.message}"

class CurrentEmployeeDeletedError(IncorrectCredentialError):
    """Exception raised when the current employee is deleted"""

    def __init__(self, deleted_employee: EmployeeEntity):
        self.message = f"The current employee with ID '{deleted_employee.id}' and email: '{deleted_employee.email}' is deleted: {deleted_employee.is_deleted}."
        super().__init__(self.message)  # Call the base class constructor

    def __str__(self):
        return f"{self.message}"

class WeakPasswordError(IncorrectCredentialError):
    """Exception raised for weak password"""

    def __init__(self, password: str, extra_info: str = ""):
        self.message = f"The password '{password}' is weak{extra_info}."
        super().__init__(self.message)  # Call the base class constructor

class IncorrectRoleError(IncorrectCredentialError):
    """Exception raised for incorrect role"""

    def __init__(self, email_of_current_employee: str, incorrect_role: Union[str, RoleEnum], correct_roles: Union[List[str], str, List[RoleEnum], RoleEnum], action: str):
        if isinstance(incorrect_role, RoleEnum):
            incorrect_role = incorrect_role.value

        is_correct_roles_a_list = isinstance(correct_roles, list)
        if is_correct_roles_a_list:
            correct_roles = [role.value if isinstance(role, RoleEnum) else role for role in correct_roles]
            correct_roles = ', '.join(correct_roles)
        else:
            correct_roles = correct_roles.value if isinstance(correct_roles, RoleEnum) else correct_roles
        self.message = f"The role '{incorrect_role}' for the employee with email: '{email_of_current_employee}' is incorrect for the action: {action}. Correct {"roles are" if is_correct_roles_a_list else "role is"}: {correct_roles}."
        super().__init__(self.message)  # Call the base class constructor

    def __str__(self):
        return f"{self.message}"

class SelfDeleteError(IncorrectCredentialError):
    """Exception raised when an employee attempts to delete itself."""

    def __init__(self, employee_id: str):
        """
        Initialize the exception with the employee's ID.

        :param employee_id: The ID of the employee attempting to delete itself.
        :type employee_id: str
        """
        self.message = f"Employee with ID '{employee_id}' cannot delete itself."
        super().__init__(self.message)

    def __str__(self):
        return self.message

    