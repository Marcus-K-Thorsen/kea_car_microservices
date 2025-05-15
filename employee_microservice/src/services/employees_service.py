# External Library imports
from typing import List, Optional

# Internal library imports
from src.logger_tool import logger
from src.entities import EmployeeMesssage
from src.database_management import Session
from src.repositories import EmployeeRepository
from src.core import (
    TokenPayload,
    get_current_employee
)
from src.resources import (
    EmployeeReturnResource,
    RoleEnum
)

from src.exceptions import (
    UnableToUndeleteAlreadyUndeletedEntityError,
    UnableToDeleteAlreadyDeletedEntityError,
    AlreadyTakenFieldValueError,
    UnableToFindIdError
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
        
    current_employee = get_current_employee(token, session, current_user_action="get_all employees")
    
    if current_employee.role == RoleEnum.sales_person:
        logger.warning(f"Sales person with ID: '{current_employee.id}' tried to get all employees.")
        logger.info("Will instead return only the current employee in a list.")
        return [current_employee.as_resource()]
    
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
    
    current_employee = get_current_employee(token, session, current_user_action="get employee by id")
    
    if current_employee.role == RoleEnum.sales_person and current_employee.id != employee_id:
        logger.warning(f"Sales person with ID: '{current_employee.id}' tried to get a different employee than themselves.")
        logger.info("Will instead return the current employee.")
        return current_employee.as_resource()

    employee = repository.get_by_id(employee_id)
    if employee is None:
        raise UnableToFindIdError(
            entity_name="Employee",
            entity_id=employee_id
        )

    return employee.as_resource()


def create(
    session: Session,
    employee_create_data: EmployeeMesssage
) -> None:

    repository = EmployeeRepository(session)
    
    if not isinstance(employee_create_data, EmployeeMesssage):
        raise TypeError(f"employee_create_data must be of type EmployeeMesssage, "
                        f"not {type(employee_create_data).__name__}.")
    
    the_employee_email_is_already_taken = repository.is_email_taken(employee_create_data.email, employee_create_data.id)
    
    if the_employee_email_is_already_taken:
        disputed_email = employee_create_data.email
        logger.warning(f"Employee with email: '{disputed_email}' already exists.")
        
        already_created_employee_with_the_same_email = repository.get_by_email(disputed_email)
        logger.error(f"Employee with ID: '{employee_create_data.id}' not created before "
                     f"Employee with ID: '{already_created_employee_with_the_same_email.id}', has its email: '{disputed_email}' updated to something else.")
        raise AlreadyTakenFieldValueError(
            entity_name="Employee",
            field="email",
            value=disputed_email
        )
    
    already_created_employee = repository.get_by_id(employee_create_data.id)

    if already_created_employee is not None:
        logger.warning(f"Employee with ID: '{employee_create_data.id}' already exists.")
        if employee_create_data.created_at > already_created_employee.updated_at:
            logger.warning(f"And the new data is more recent: {employee_create_data.created_at.strftime("%d/%m/%Y, %H:%M:%S")}, " 
                           f"than the past data from: {already_created_employee.updated_at.strftime("%d/%m/%Y, %H:%M:%S")}.")
            repository.update(employee_create_data)
            logger.info(f"Employee with ID: '{employee_create_data.id}' updated.")
        else:
            logger.warning(f"And the new data is NOT more recent: {employee_create_data.created_at.strftime("%d/%m/%Y, %H:%M:%S")}, " 
                           f"than the past data from: {already_created_employee.created_at.strftime("%d/%m/%Y, %H:%M:%S")}.")
            logger.info("The newly created Employee data will not be created, as the past data is more recent.")
        return None
    
    repository.create(employee_create_data)
    logger.info(f"Employee with ID: '{employee_create_data.id}' created.")
    return None


def update(
    session: Session,
    employee_update_data: EmployeeMesssage
) -> None:

    repository = EmployeeRepository(session)
        
    if not isinstance(employee_update_data, EmployeeMesssage):
        raise TypeError(f"employee_update_data must be of type EmployeeMesssage, "
                        f"not {type(employee_update_data).__name__}.")
        
    the_employee_email_is_already_taken = repository.is_email_taken(employee_update_data.email, employee_update_data.id)
    if the_employee_email_is_already_taken:
        disputed_email = employee_update_data.email
        logger.warning(f"Employee with email: '{disputed_email}' already exists.")
        
        already_created_employee_with_the_same_email = repository.get_by_email(disputed_email)
        logger.error(f"Employee with ID: '{employee_update_data.id}' not updated before "
                     f"Employee with ID: '{already_created_employee_with_the_same_email.id}', has its email: '{disputed_email}' updated to something else.")
        logger.error(f"Will assume the employee with ID: '{already_created_employee_with_the_same_email.id}' has not been updated yet, and should be tried again later, when it is.")
        raise AlreadyTakenFieldValueError(
            entity_name="Employee",
            field="email",
            value=disputed_email
        )
        
    existing_employee = repository.get_by_id(employee_update_data.id)
    if existing_employee is None:
        logger.warning(f"Employee with ID: '{employee_update_data.id}' does not exist to update.")
        repository.create(employee_update_data)
        logger.info(f"Employee with ID: '{employee_update_data.id}' updated by being created.")
        return None
    
    
    
    if employee_update_data.updated_at <= existing_employee.updated_at:
        logger.warning(f"Employee with ID: '{employee_update_data.id}' already exists.")
        logger.warning(f"And the new updated data is NOT more recent: {employee_update_data.updated_at.strftime("%d/%m/%Y, %H:%M:%S")}, " 
                       f"than the past updated data from: {existing_employee.updated_at.strftime("%d/%m/%Y, %H:%M:%S")}.")
        logger.info("The newly updated Employee data will not be updated, as the past data is more recent.")
        return None
    
    employee_update_data.is_deleted = existing_employee.is_deleted
        
    repository.update(employee_update_data)
    logger.info(f"Employee with ID: '{employee_update_data.id}' updated.")
    return None


def delete(
    session: Session,
    employee_to_delete: EmployeeMesssage
) -> None:
    
    repository = EmployeeRepository(session)
    
    if not isinstance(employee_to_delete, EmployeeMesssage):
        raise TypeError(f"employee_to_delete must be of type EmployeeMesssage, "
                        f"not {type(employee_to_delete).__name__}.")
    
    already_existing_employee_to_delete = repository.get_by_id(employee_to_delete.id)
    if already_existing_employee_to_delete is None:
        logger.warning(f"Employee with ID: '{employee_to_delete.id}' does not exist to be deleted.")
        logger.error("Will assume the employee has not been created yet, and should be tried again later, when it is.")
        raise UnableToFindIdError(
            entity_name="Employee",
            entity_id=employee_to_delete.id
        )
    
    if already_existing_employee_to_delete.is_deleted:
        logger.warning(f"Employee with ID: '{employee_to_delete.id}' is already deleted.")
        if employee_to_delete.updated_at > already_existing_employee_to_delete.updated_at:
            logger.warning(f"And the new data is more recent: {employee_to_delete.updated_at.strftime("%d/%m/%Y, %H:%M:%S")}, "
                           f"than the past data from: {already_existing_employee_to_delete.updated_at.strftime("%d/%m/%Y, %H:%M:%S")}.")
            repository.update(employee_to_delete)
            logger.info(f"Employee with ID: '{employee_to_delete.id}' is deleted by being updated.")
            return None
        else:
            logger.warning(f"And the new data is NOT more recent: {employee_to_delete.updated_at.strftime("%d/%m/%Y, %H:%M:%S")}, "
                           f"than the past data from: {already_existing_employee_to_delete.updated_at.strftime("%d/%m/%Y, %H:%M:%S")}.")
            logger.error("Will assume the employee has not been undeleted yet, and should be tried again later, when it is.")
            raise UnableToDeleteAlreadyDeletedEntityError(
                entity_name="Employee",
                entity_id=employee_to_delete.id
            )
    
    repository.delete(already_existing_employee_to_delete)
    logger.info(f"Employee with ID: '{employee_to_delete.id}' is deleted.")
    return None


def undelete(
    session: Session,
    employee_to_undelete: EmployeeMesssage
) -> None:

    repository = EmployeeRepository(session)
    
    if not isinstance(employee_to_undelete, EmployeeMesssage):
        raise TypeError(f"employee_to_undelete must be of type EmployeeMesssage, "
                        f"not {type(employee_to_undelete).__name__}.")
    
    already_existing_employee_to_undelete = repository.get_by_id(employee_to_undelete.id)
    if already_existing_employee_to_undelete is None:
        logger.warning(f"Employee with ID: '{employee_to_undelete.id}' does not exist to be undeleted.")
        logger.info("Will instead create the employee.")
        repository.create(employee_to_undelete)
        logger.info(f"Employee with ID: '{employee_to_undelete.id}' undeleted by being created.")
        return None
    
    if not already_existing_employee_to_undelete.is_deleted:
        logger.warning(f"Employee with ID: '{employee_to_undelete.id}' is not deleted.")
        if employee_to_undelete.updated_at > already_existing_employee_to_undelete.updated_at:
            logger.warning(f"And the new data is more recent: {employee_to_undelete.updated_at.strftime("%d/%m/%Y, %H:%M:%S")}, "
                           f"than the past data from: {already_existing_employee_to_undelete.updated_at.strftime("%d/%m/%Y, %H:%M:%S")}.")
            logger.info("Will instead update the employee.")
            repository.update(employee_to_undelete)
            logger.info(f"Employee with ID: '{employee_to_undelete.id}' is undeleted by being updated.")
            return None
        else:
            logger.warning(f"And the new data is NOT more recent: {employee_to_undelete.updated_at.strftime("%d/%m/%Y, %H:%M:%S")}, "
                           f"than the past data from: {already_existing_employee_to_undelete.updated_at.strftime("%d/%m/%Y, %H:%M:%S")}.")
            logger.error("Will assume the employee has not been undeleted yet, and should be tried again later, when it is.")
            raise UnableToUndeleteAlreadyUndeletedEntityError(
                entity_name="Employee",
                entity_id=employee_to_undelete.id
            )
    
    repository.undelete(already_existing_employee_to_undelete)
    logger.info(f"Employee with ID: '{employee_to_undelete.id}' is undeleted.")
    return None

