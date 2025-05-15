# External Library imports


# Internal library imports
from src.logger_tool import logger
from src.database_management import Database
from src.repositories import InsuranceRepository
from src.entities import InsuranceMessage
from src.exceptions import AlreadyTakenFieldValueError




def create(
        database: Database,
        insurance_create_data: InsuranceMessage
) -> None:

    repository = InsuranceRepository(database)
    
    if not isinstance(insurance_create_data, InsuranceMessage):
        raise TypeError(f"insurance_create_data must be of type InsuranceMessage, "
                        f"not {type(insurance_create_data).__name__}.")

    
    existing_insurance_with_the_same_name = repository.get_by_name(insurance_create_data.name, insurance_create_data.id)
    if existing_insurance_with_the_same_name is not None:
        logger.warning(f"Insurance with name {insurance_create_data.name} already exists.")
        logger.error("Will assume the insurance before has not had its name updated or has not been removed yet, so will have the try again later")
        raise AlreadyTakenFieldValueError(
            field_name="name",
            field_value=insurance_create_data.name,
            entity_name="Insurance"
        )
    
    already_created_insurance = repository.get_by_id(insurance_create_data.id)
    if already_created_insurance is not None:
        logger.warning(f"Insurance with id {insurance_create_data.id} already exists.")
        if insurance_create_data.created_at > already_created_insurance.updated_at:
            logger.info(f"Insurance with id {insurance_create_data.id} will be updated.")
            logger.info(f"As the already existing insurance has not been updated since {already_created_insurance.updated_at}, "
                        f"the new insurance will be created as it was created in the future {insurance_create_data.created_at}.")
            repository.update(insurance_create_data)
            logger.info(f"Insurance with id {insurance_create_data.id} has been created by being updated.")
            return None
    
    repository.create(insurance_create_data)
    return None


def update(
        database: Database,
        insurance_update_data: InsuranceMessage
) -> None:

    repository = InsuranceRepository(database)
    
    if not isinstance(insurance_update_data, InsuranceMessage):
        raise TypeError(f"insurance_update_data must be of type InsuranceMessage, "
                        f"not {type(insurance_update_data).__name__}.")
    
    is_name_already_taken = repository.get_by_name(insurance_update_data.name, insurance_update_data.id)
    if is_name_already_taken is not None:
        logger.warning(f"Insurance with name {insurance_update_data.name} already exists.")
        logger.error("Will assume the insurance before has not had its name updated or has not been removed yet, so will have the try again later")
        raise AlreadyTakenFieldValueError(
            field_name="name",
            field_value=insurance_update_data.name,
            entity_name="Insurance"
        )
    
    updated_insurance = repository.update(insurance_update_data)
    
    if updated_insurance is None:
        logger.warning(f"Insurance with id {insurance_update_data.id} does not exist.")
        logger.info("Will assume that the insurance has not been created yet, so will be updating by creating the insurance.")
        repository.create(insurance_update_data)
        logger.info(f"Insurance with id {insurance_update_data.id} has been updated by being created.")
        return None
    
    logger.info(f"Insurance with id {insurance_update_data.id} has been updated.")
    return None
