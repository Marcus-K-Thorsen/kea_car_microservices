# External Library imports
from typing import List, Optional
from pydantic import EmailStr

# Internal library imports
from src.database_management import Session
from src.repositories import EmployeeRepository
from src.core import (
    TokenPayload, 
    get_current_employee, 
    is_password_pwned, 
    is_password_to_short,
    get_password_hash
)
from src.exceptions import (
    AlreadyTakenFieldValueError,
    UnableToFindIdError,
    WeakPasswordError,
    SelfDeleteError,
    SelfDemotionError
)
from src.resources import (
    EmployeeCreateResource, 
    EmployeeUpdateResource, 
    EmployeeReturnResource, 
    RoleEnum
)
from src.message_broker_management import (
    publish_employee_created_message,
    publish_employee_updated_message,
    publish_employee_deleted_message,
    publish_employee_undeleted_message
)


def get_all(
    session: Session,
    token: TokenPayload,
    employee_limit: Optional[int] = None,
    is_deleted_filter: Optional[bool] = None
) -> List[EmployeeReturnResource]:
    
    repository = EmployeeRepository(session)
    
    
    if isinstance(employee_limit, bool) or not (isinstance(employee_limit, int) or employee_limit is None):
        raise TypeError(f"employee_limit must be of type int or None, "
                        f"not {type(employee_limit).__name__}.")
    
    if not isinstance(is_deleted_filter, bool) and is_deleted_filter is not None:
        raise TypeError(f"is_deleted_filter must be of type bool or None, "
                        f"not {type(is_deleted_filter).__name__}.")
        
    get_current_employee(token, session, current_user_action="get_all employees", valid_roles=RoleEnum.admin)

    
    employees = repository.get_all(limit=employee_limit, deletion_filter=is_deleted_filter)
    
    return [employee.as_resource() for employee in employees]


def get_by_id(
    session: Session,
    token: TokenPayload,
    employee_id: str
) -> EmployeeReturnResource:

    repository = EmployeeRepository(session)
    
    if not isinstance(employee_id, str):
        raise TypeError(f"employee_id must be of type str, "
                        f"not {type(employee_id).__name__}.")
    
    get_current_employee(token, session, current_user_action="get employee by id", valid_roles=RoleEnum.admin)

    employee = repository.get_by_id(employee_id)
    if employee is None:
        raise UnableToFindIdError(
            entity_name="Employee",
            entity_id=employee_id
        )

    return employee.as_resource()


def create(
    session: Session,
    token: TokenPayload,
    employee_create_data: EmployeeCreateResource
) -> EmployeeReturnResource:

    repository = EmployeeRepository(session)
    
    if not isinstance(employee_create_data, EmployeeCreateResource):
        raise TypeError(f"employee_create_data must be of type EmployeeCreateResource, "
                        f"not {type(employee_create_data).__name__}.")
        
    get_current_employee(token, session, current_user_action="create employee", valid_roles=RoleEnum.admin)
    
    already_created_employee = repository.get_by_id(employee_create_data.id)
    if already_created_employee is not None:
        return already_created_employee.as_resource()

    if repository.is_email_taken(str(employee_create_data.email)):
        raise AlreadyTakenFieldValueError(
            entity_name="Employee",
            field="email",
            value=str(employee_create_data.email)
        )
    
    if is_password_to_short(employee_create_data.password):
        raise WeakPasswordError(
            password=employee_create_data.password,
            extra_info=": Password must be at least 8 characters long"
        )
    
    if is_password_pwned(employee_create_data.password):
        raise WeakPasswordError(
            password=employee_create_data.password,
            extra_info=": Password has been registered as having been pwned, please choose a stronger password"
        )
    
    hashed_password = get_password_hash(employee_create_data.password)
    
    created_employee = repository.create(employee_create_data, hashed_password)
    
    employee_as_resource = created_employee.as_resource()
    
    publish_employee_created_message(created_employee)
    
    return employee_as_resource


def update(
    session: Session,
    token: TokenPayload,
    employee_id: str,
    employee_update_data: EmployeeUpdateResource
) -> EmployeeReturnResource:

    repository = EmployeeRepository(session)
    
    if not isinstance(employee_id, str):
        raise TypeError(f"employee_id must be of type str, "
                        f"not {type(employee_id).__name__}.")
        
    if not isinstance(employee_update_data, EmployeeUpdateResource):
        raise TypeError(f"employee_update_data must be of type EmployeeUpdateResource, "
                        f"not {type(employee_update_data).__name__}.")
        
    current_employee = get_current_employee(token, session, current_user_action="update employee", valid_roles=[RoleEnum.admin])
    
    if current_employee.id == employee_id and employee_update_data.role is not None and employee_update_data.role != RoleEnum.admin:
        raise SelfDemotionError(current_employee, employee_update_data.role)
    
    employee_email_to_update: Optional[EmailStr] = employee_update_data.email
    
    if employee_email_to_update is not None and repository.is_email_taken(str(employee_email_to_update), employee_id):
        raise AlreadyTakenFieldValueError(
            entity_name="Employee",
            field="email",
            value=str(employee_email_to_update)
        )
    
    updated_password: Optional[str] = employee_update_data.password
    if updated_password is not None:
        if is_password_to_short(updated_password):
            raise WeakPasswordError(
                password=updated_password,
                extra_info=": Password must be at least 8 characters long"
            )
        
        if is_password_pwned(updated_password):
            raise WeakPasswordError(
                password=updated_password,
                extra_info=": Password has been registered as having been pwned, please choose a stronger password"
            )
        
        updated_password = get_password_hash(updated_password)
        
        
    updated_employee = repository.update(employee_id, employee_update_data, updated_password)
    if updated_employee is None:
        raise UnableToFindIdError(
            entity_name="Employee",
            entity_id=employee_id
        )
    
    employee_as_resource = updated_employee.as_resource()
    
    publish_employee_updated_message(updated_employee)
    
    return employee_as_resource


def delete(
    session: Session,
    token: TokenPayload,
    employee_id: str
) -> EmployeeReturnResource:
    
    repository = EmployeeRepository(session)
    
    if not isinstance(employee_id, str):
        raise TypeError(f"employee_id must be of type str, "
                        f"not {type(employee_id).__name__}.")
        
    current_employee = get_current_employee(token, session, current_user_action="delete employee", valid_roles=RoleEnum.admin)
    
    if current_employee.id == employee_id:
        raise SelfDeleteError(employee_id)
    
    employee_to_delete = repository.get_by_id(employee_id)
    if employee_to_delete is None:
        raise UnableToFindIdError(
            entity_name="Employee",
            entity_id=employee_id
        )
        
    if employee_to_delete.is_deleted:
        return employee_to_delete.as_resource()

    deleted_employee = repository.delete(employee_to_delete)
    
    employee_as_resource = deleted_employee.as_resource()
    
    publish_employee_deleted_message(deleted_employee)
    
    return employee_as_resource


def undelete(
    session: Session,
    token: TokenPayload,
    employee_id: str
) -> EmployeeReturnResource:

    repository = EmployeeRepository(session)
    
    if not isinstance(employee_id, str):
        raise TypeError(f"employee_id must be of type str, "
                        f"not {type(employee_id).__name__}.")
        
    get_current_employee(token, session, current_user_action="undelete employee", valid_roles=RoleEnum.admin)
    
    employee_to_undelete = repository.get_by_id(employee_id)
    if employee_to_undelete is None:
        raise UnableToFindIdError(
            entity_name="Employee",
            entity_id=employee_id
        )
    
    if not employee_to_undelete.is_deleted:
        return employee_to_undelete.as_resource()

    undeleted_employee = repository.undelete(employee_to_undelete)
    employee_as_resource = undeleted_employee.as_resource()
    
    publish_employee_undeleted_message(undeleted_employee)
    
    return employee_as_resource