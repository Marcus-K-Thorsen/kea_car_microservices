# External Library imports
from pydantic import EmailStr
from typing import List, Optional

# Internal library imports
from src.database_management import Session
from src.repositories import CustomerRepository
from src.exceptions import UnableToFindIdError, AlreadyTakenFieldValueError
from src.core import (
    TokenPayload, 
    get_current_employee
)
from src.resources import (
    CustomerReturnResource, 
    CustomerCreateResource, 
    CustomerUpdateResource,
    RoleEnum
)



def get_all(
        session: Session,
        token: TokenPayload,
        filter_customer_by_email: Optional[str] = None,
        customer_limit: Optional[int] = None
) -> List[CustomerReturnResource]:

    repository = CustomerRepository(session)
    
    if not (isinstance(filter_customer_by_email, str) or filter_customer_by_email is None):
        raise TypeError(f"filter_customer_by_email must be of type str or None, "
                        f"not {type(filter_customer_by_email).__name__}.")
    if isinstance(customer_limit, bool) or not (isinstance(customer_limit, int) or customer_limit is None):
        raise TypeError(f"customer_limit must be of type int or None, "
                        f"not {type(customer_limit).__name__}.")
        
    get_current_employee(
        token,
        session,
        current_user_action="get_all customers"
    )
    
    customers = repository.get_all(filter_customer_by_email, customer_limit)
    
    return [customer.as_resource() for customer in customers]


def get_by_id(
        session: Session,
        token: TokenPayload,
        customer_id: str
) -> CustomerReturnResource:

    repository = CustomerRepository(session)
    
    if not isinstance(customer_id, str):
        raise TypeError(f"customer_id must be of type str, "
                        f"not {type(customer_id).__name__}.")
        
    get_current_employee(
        token,
        session,
        current_user_action="get customer by id"
    )

    customer = repository.get_by_id(customer_id)
    
    if customer is None:
        raise UnableToFindIdError(
            entity_name="Customer",
            entity_id=customer_id
        )
    return customer


def create(
        session: Session,
        token: TokenPayload,
        customer_create_data: CustomerCreateResource
) -> CustomerReturnResource:

    repository = CustomerRepository(session)
    
    if not isinstance(customer_create_data, CustomerCreateResource):
        raise TypeError(f"customer_create_data must be of type CustomerCreateResource, "
                        f"not {type(customer_create_data).__name__}.")
        
    get_current_employee(
        token,
        session,
        current_user_action="create customer"
    )
    
    already_created_customer = repository.get_by_id(str(customer_create_data.id))
    if already_created_customer is not None:
        return already_created_customer.as_resource()

    if repository.is_email_taken(
        email=str(customer_create_data.email)
    ):
        raise AlreadyTakenFieldValueError(
            entity_name="Customer",
            field="email",
            value=str(customer_create_data.email)
        )
    
    newly_created_customer = repository.create(customer_create_data)

    return newly_created_customer.as_resource()


def update(
        session: Session,
        token: TokenPayload,
        customer_id: str,
        customer_update_data: CustomerUpdateResource
) -> CustomerReturnResource:

    repository = CustomerRepository(session)
    
    if not isinstance(customer_id, str):
        raise TypeError(f"customer_id must be of type str, "
                        f"not {type(customer_id).__name__}.")
    if not isinstance(customer_update_data, CustomerUpdateResource):
        raise TypeError(f"customer_update_data must be of type CustomerUpdateResource, "
                        f"not {type(customer_update_data).__name__}.")
        
    get_current_employee(
        token,
        session,
        current_user_action="update customer"
    )
    
    customer_email_to_update: Optional[EmailStr] = customer_update_data.email

    if customer_email_to_update is not None and repository.is_email_taken(str(customer_email_to_update), customer_id):
        raise AlreadyTakenFieldValueError(
            entity_name="Customer",
            field="email",
            value=str(customer_email_to_update)
        )

    updated_customer = repository.update(customer_id, customer_update_data)
    if updated_customer is None:
        raise UnableToFindIdError(
            entity_name="Customer",
            entity_id=customer_id
        )

    return updated_customer.as_resource()


def delete(
        session: Session,
        token: TokenPayload,
        customer_id: str
) -> None:

    repository = CustomerRepository(session)
    
    if not isinstance(customer_id, str):
        raise TypeError(f"customer_id must be of type str, "
                        f"not {type(customer_id).__name__}.")
        
    get_current_employee(
        token,
        session,
        current_user_action="delete customer",
        valid_roles=[RoleEnum.admin, RoleEnum.manager]
    )

    customer = repository.get_by_id(customer_id)
    if customer is None:
        raise UnableToFindIdError(
            entity_name="Customer",
            entity_id=customer_id
        )
        
    repository.delete(customer)
