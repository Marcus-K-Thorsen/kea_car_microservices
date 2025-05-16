# External Library imports
from typing import List, Optional

# Internal library imports
from src.database_management import Session
from src.repositories import InsuranceRepository
from src.resources import (
    InsuranceReturnResource,
    InsuranceCreateResource,
    InsuranceUpdateResource,
    RoleEnum
)
from src.core import (
    TokenPayload, 
    get_current_employee
)
from src.exceptions import UnableToFindIdError, AlreadyTakenFieldValueError
from src.message_broker_management import (
    publish_insurance_created_message,
    publish_insurance_updated_message
)


def get_all(
        session: Session,
        token: TokenPayload,
        insurance_limit: Optional[int] = None
) -> List[InsuranceReturnResource]:

    repository = InsuranceRepository(session)
    
    if isinstance(insurance_limit, bool) or not (isinstance(insurance_limit, int) or insurance_limit is None):
        raise TypeError(f"insurance_limit must be of type int or None, "
                        f"not {type(insurance_limit).__name__}.")

    get_current_employee(
        token,
        session,
        current_user_action="get_all insurances"
    )
    
    insurances = repository.get_all(insurance_limit)
    
    return [insurance.as_resource() for insurance in insurances]

def get_by_id(
        session: Session,
        token: TokenPayload,
        insurance_id: str
) -> InsuranceReturnResource:

    repository = InsuranceRepository(session)

    if not isinstance(insurance_id, str):
        raise TypeError(f"insurance_id must be of type str, "
                        f"not {type(insurance_id).__name__}.")

    get_current_employee(
        token,
        session,
        current_user_action="get insurance by id"
    )
    
    insurance = repository.get_by_id(insurance_id)
    
    if insurance is None:
        raise UnableToFindIdError(
            entity_name="Insurance",
            entity_id=insurance_id
        )
    
    return insurance.as_resource()


def create(
        session: Session,
        token: TokenPayload,
        insurance_create_data: InsuranceCreateResource
) -> InsuranceReturnResource:

    repository = InsuranceRepository(session)
    
    if not isinstance(insurance_create_data, InsuranceCreateResource):
        raise TypeError(f"insurance_create_data must be of type InsuranceCreateResource, "
                        f"not {type(insurance_create_data).__name__}.")

    get_current_employee(
        token,
        session,
        current_user_action="create insurance",
        valid_roles=[RoleEnum.admin, RoleEnum.manager]
    )
    
    is_name_already_taken = repository.get_by_name(insurance_create_data.name, insurance_create_data.id)
    if is_name_already_taken is not None:
        raise AlreadyTakenFieldValueError(
            field_name="name",
            field_value=insurance_create_data.name,
            entity_name="Insurance"
        )
    
    already_created_insurance = repository.get_by_id(insurance_create_data.id)
    if already_created_insurance is not None:
        return already_created_insurance.as_resource()
    
    insurance = repository.create(insurance_create_data)
    insurance_as_resource = insurance.as_resource()
    
    publish_insurance_created_message(insurance)
    
    return insurance_as_resource


def update(
        session: Session,
        token: TokenPayload,
        insurance_id: str,
        insurance_update_data: InsuranceUpdateResource
) -> InsuranceReturnResource:

    repository = InsuranceRepository(session)
    
    if not isinstance(insurance_id, str):
        raise TypeError(f"insurance_id must be of type str, "
                        f"not {type(insurance_id).__name__}.")
    if not isinstance(insurance_update_data, InsuranceUpdateResource):
        raise TypeError(f"insurance_update_data must be of type InsuranceUpdateResource, "
                        f"not {type(insurance_update_data).__name__}.")

    get_current_employee(
        token,
        session,
        current_user_action="update insurance",
        valid_roles=[RoleEnum.admin, RoleEnum.manager]
    )
    
    is_name_already_taken = repository.get_by_name(insurance_update_data.name, insurance_id)
    if is_name_already_taken is not None:
        raise AlreadyTakenFieldValueError(
            field_name="name",
            field_value=insurance_update_data.name,
            entity_name="Insurance"
        )
    
    updated_insurance = repository.update(insurance_id, insurance_update_data)
    
    if updated_insurance is None:
        raise UnableToFindIdError(
            entity_name="Insurance",
            entity_id=insurance_id
        )
    
    insurance_as_resource = updated_insurance.as_resource()
        
    publish_insurance_updated_message(updated_insurance)
    
    return insurance_as_resource
