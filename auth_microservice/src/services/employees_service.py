# External Library imports


# Internal library imports
from src.logger_tool import logger
from src.entities import EmployeeEntity
from src.database_management import Database
from src.repositories import EmployeeRepository

from src.exceptions import (
    UnableToUndeleteAlreadyUndeletedEntityError,
    AlreadyTakenFieldValueError,
    UnableToFindIdError
)


def create(
    database: Database,
    employee_create_data: EmployeeEntity
) -> None:

    repository = EmployeeRepository(database)
    
    if not isinstance(employee_create_data, EmployeeEntity):
        raise TypeError(f"employee_create_data must be of type EmployeeEntity, "
                        f"not {type(employee_create_data).__name__}.")
        
    employee_email_is_already_taken = repository.is_email_taken(employee_create_data.email, employee_create_data.id)
    if employee_email_is_already_taken:
        disputed_email = employee_create_data.email
        already_created_employee_with_the_same_email = repository.get_by_email(disputed_email)
        logger.warning(f"Employee with email: '{disputed_email}' already exists.")
        if already_created_employee_with_the_same_email and employee_create_data.created_at > already_created_employee_with_the_same_email.updated_at:
            logger.warning(f"And the new data is more recent: {employee_create_data.created_at.strftime("%d/%m/%Y, %H:%M:%S")}, " 
                           f"than the past data from: {already_created_employee_with_the_same_email.updated_at.strftime("%d/%m/%Y, %H:%M:%S")}.")
            repository.delete(already_created_employee_with_the_same_email)
            logger.info(f"Past Employee with email: '{disputed_email}' and ID: '{already_created_employee_with_the_same_email.id}' is deleted.")
            repository.create(employee_create_data)
            logger.info(f"Employee with ID: '{employee_create_data.id}' created in its stead.")
            return None
        else:
            logger.warning(f"And the new data is NOT more recent: {employee_create_data.created_at.strftime("%d/%m/%Y, %H:%M:%S")}, " 
                           f"than the past data from: {already_created_employee_with_the_same_email.updated_at.strftime("%d/%m/%Y, %H:%M:%S")}.")
            logger.error(f"Employee with ID: '{employee_create_data.id}' not created before "
                         f"Employee with ID: '{already_created_employee_with_the_same_email.id}', "
                         f"is deleted or has its email updated to something else, and should be tried again later, when it is..")
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
            logger.info(f"Employee with ID: '{employee_create_data.id}' created by being updated.")
            return None
        else:
            logger.warning(f"And the new data is NOT more recent: {employee_create_data.created_at.strftime("%d/%m/%Y, %H:%M:%S")}, " 
                           f"than the past data from: {already_created_employee.updated_at.strftime("%d/%m/%Y, %H:%M:%S")}.")
            logger.info("The newly created Employee data will not be created, as the past data is more recent.")
            return None
    
    repository.create(employee_create_data)
    logger.info(f"Employee with ID: '{employee_create_data.id}' created.")
    return None


def update(
    database: Database,
    employee_update_data: EmployeeEntity
) -> None:

    repository = EmployeeRepository(database)
        
    if not isinstance(employee_update_data, EmployeeEntity):
        raise TypeError(f"employee_update_data must be of type EmployeeEntity, "
                        f"not {type(employee_update_data).__name__}.")
    
    existing_employee_with_the_same_email = repository.get_by_email(employee_update_data.email)
    if existing_employee_with_the_same_email is not None and existing_employee_with_the_same_email.id != employee_update_data.id:
        logger.warning(f"A different Employee with email: '{employee_update_data.email}' already exists.")
        if employee_update_data.updated_at > existing_employee_with_the_same_email.updated_at:
            logger.warning(f"And the new updated data is more recent: {employee_update_data.updated_at.strftime("%d/%m/%Y, %H:%M:%S")}, " 
                           f"than the existing updated data from: {existing_employee_with_the_same_email.updated_at.strftime("%d/%m/%Y, %H:%M:%S")}.")
            repository.delete(existing_employee_with_the_same_email)
            logger.info(f"Existing Employee with email: '{existing_employee_with_the_same_email.email}' and ID: '{existing_employee_with_the_same_email.id}' is deleted.")
            repository.create(employee_update_data)
            logger.info(f"Employee with ID: '{employee_update_data.id}' is updated by being created in its stead.")
            return None
        else:
            logger.warning(f"And the updated data is NOT more recent: {employee_update_data.updated_at.strftime("%d/%m/%Y, %H:%M:%S")}, " 
                           f"than the past data from: {existing_employee_with_the_same_email.updated_at.strftime("%d/%m/%Y, %H:%M:%S")}.")
            logger.error(f"Employee with ID: '{employee_update_data.id}' not updated before "
                         f"Employee with ID: '{existing_employee_with_the_same_email.id}', "
                         f"is deleted or has its email updated to something else, and should be tried again later, when it is..")
            raise AlreadyTakenFieldValueError(
                entity_name="Employee",
                field="email",
                value=employee_update_data.email
            )
            
    already_updated_employee = repository.get_by_id(employee_update_data.id)
    if already_updated_employee is None:
        logger.warning(f"Employee with ID: '{employee_update_data.id}' does not exist to update.")
        repository.create(employee_update_data)
        logger.info(f"Employee with ID: '{employee_update_data.id}' is updated by being created.")
        return None
    
    if employee_update_data.updated_at <= already_updated_employee.updated_at:
        logger.warning(f"Employee with ID: '{employee_update_data.id}' already exists.")
        logger.warning(f"And the new updated data is NOT more recent: {employee_update_data.updated_at.strftime("%d/%m/%Y, %H:%M:%S")}, " 
                       f"than the already updated data from: {already_updated_employee.updated_at.strftime("%d/%m/%Y, %H:%M:%S")}.")
        logger.info("The newly updated Employee data will not be updated, as the already updated data is more recent.")
        return None
        
    repository.update(employee_update_data)
    logger.info(f"Employee with ID: '{employee_update_data.id}' updated.")
    return None


def delete(
    database: Database,
    employee_to_delete: EmployeeEntity
) -> None:
    
    repository = EmployeeRepository(database)
    
    if not isinstance(employee_to_delete, EmployeeEntity):
        raise TypeError(f"employee_to_delete must be of type EmployeeEntity, "
                        f"not {type(employee_to_delete).__name__}.")
        
    employee_id = employee_to_delete.id

    is_employee_deleted = repository.delete(employee_id)
    
    if not is_employee_deleted:
        logger.warning(f"Employee with ID: '{employee_id}' does not exist to be deleted.")
        logger.error("Will assume the employee has not been created yet, and should be tried again later, when it is.")
        raise UnableToFindIdError(
            entity_name="Employee",
            entity_id=employee_id
        )
    
    logger.info(f"Employee with ID: '{employee_id}' deleted.")
    return None


def undelete(
    database: Database,
    employee_to_undelete: EmployeeEntity
) -> None:

    repository = EmployeeRepository(database)
    
    if not isinstance(employee_to_undelete, EmployeeEntity):
        raise TypeError(f"employee_to_undelete must be of type EmployeeEntity, "
                        f"not {type(employee_to_undelete).__name__}.")
        
    is_employee_email_already_taken_by_another_employee = repository.is_email_taken(employee_to_undelete.email, employee_to_undelete.id)
    
    if is_employee_email_already_taken_by_another_employee:
        disputed_email = employee_to_undelete.email
        logger.warning(f"A different Employee with email: '{disputed_email}' already exists.")
        logger.error(f"Employee with ID: '{employee_to_undelete.id}' is not undeleted "
                     f"before the email: '{disputed_email}' is not taken by another employee, and should be tried again later, when it is available.")
        raise AlreadyTakenFieldValueError(
            entity_name="Employee",
            field="email",
            value=disputed_email
        )
    
    already_existing_employee_to_undelete = repository.get_by_id(employee_to_undelete.id)
    if already_existing_employee_to_undelete is not None:
        logger.warning(f"Employee with ID: '{employee_to_undelete.id}' already exists and has therfore not been deleted yet.")
        logger.error("Will assume the employee has not been deleted yet, and should be tried again later, when it is.")
        raise UnableToUndeleteAlreadyUndeletedEntityError(
            entity_name="Employee",
            entity_id=employee_to_undelete.id
        )
    
    repository.create(employee_to_undelete)
    logger.info(f"Employee with ID: '{employee_to_undelete.id}' undeleted by being created.")
    return None

