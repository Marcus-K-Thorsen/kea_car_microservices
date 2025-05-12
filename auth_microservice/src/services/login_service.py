# External Library imports


# Internal library imports
from src.database_management import Database
from src.core import Token, create_access_token, verify_password
from src.exceptions import IncorrectEmailError, IncorrectPasswordError
from src.repositories import EmployeeRepository
from src.resources import EmployeeLoginResource

def login(
        database: Database,
        employee_login_data: EmployeeLoginResource
) -> Token:

    repository = EmployeeRepository(database)
    if not isinstance(employee_login_data, EmployeeLoginResource):
        raise TypeError(f"employee_login_data must be of type EmployeeLoginResource, "
                        f"not {type(employee_login_data).__name__}.")

    employee = repository.get_by_email(employee_login_data.email)
    if employee is None:
        raise IncorrectEmailError(
            email=employee_login_data.email
        )
    
    if not verify_password(
            sent_login_password=employee_login_data.password,
            found_hashed_password=employee.hashed_password
    ):
        raise IncorrectPasswordError(
            email=employee.email,
            password=employee_login_data.password
        )

    return create_access_token(employee.as_resource())