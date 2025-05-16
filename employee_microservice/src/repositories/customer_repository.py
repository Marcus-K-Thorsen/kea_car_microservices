# External Library imports
from typing import Optional, List


# Internal library imports
from src.entities import CustomerEntity
from src.resources import (
    CustomerCreateResource,
    CustomerUpdateResource
)
from src.repositories.base_repository import BaseRepository



class CustomerRepository(BaseRepository):
    
    def get_all(
            self,
            email_filter: Optional[str] = None,
            limit: Optional[int] = None
    ) -> List[CustomerEntity]:
        """
        Retrieves a list of customers from the Employee MySQL database.
        
        :param email_filter: Filter for customers by email (optional).
        :type email_filter: str | None
        :param limit: The maximum number of customers to retrieve (optional).
        :type limit: int | None
        :return: A list of customers.
        :rtype: List[CustomerEntity]
        """
        customers_query = self.session.query(CustomerEntity)
        if email_filter is not None and isinstance(email_filter, str):
            customers_query = customers_query.filter(CustomerEntity.email.contains(email_filter))
        if self.limit_is_valid(limit):
            customers_query = customers_query.limit(limit)
        return customers_query.all()
    

    def get_by_id(
            self,
            customer_id: str
    ) -> Optional[CustomerEntity]:
        """
        Retrieves a customer by ID from the Employee MySQL database.
        
        :param customer_id: The ID of the customer to retrieve.
        :type customer_id: str
        :return: The customer if found, None otherwise.
        :rtype: CustomerEntity | None
        """
        return self.session.get(CustomerEntity, customer_id)


    def create(
            self,
            customer_create_data: CustomerCreateResource
    ) -> CustomerEntity:
        """
        Creates a new customer in the Employee MySQL database.
        
        :param customer_create_data: The data for the customer to create.
        :type customer_create_data: CustomerCreateResource
        :return: The created customer entity.
        :rtype: CustomerEntity
        """
        new_customer = CustomerEntity(
            id=str(customer_create_data.id),
            email=str(customer_create_data.email),
            phone_number=customer_create_data.phone_number,
            first_name=customer_create_data.first_name,
            last_name=customer_create_data.last_name,
            address=customer_create_data.address,
        )
        self.session.add(new_customer)
        self.session.flush()
        self.session.refresh(new_customer)

        return new_customer

    def update(
            self,
            customer_id: str,
            customer_update_data: CustomerUpdateResource
    ) -> Optional[CustomerEntity]:

        customer = self.session.get(CustomerEntity, customer_id)
        if customer is None:
            return None

        for key, value in customer_update_data.get_updated_fields().items():
            if key == "email":
                value = str(value)
            setattr(customer, key, value)

        self.session.flush()
        self.session.refresh(customer)

        return customer

    def delete(
            self,
            customer: CustomerEntity
    ) -> None:
        """
        Deletes a customer from the Employee MySQL database.
        
        :param customer: The customer to delete.
        :type customer: CustomerEntity
        :return: None
        :rtype: None
        """
        self.session.query(CustomerEntity).filter_by(id=customer.id).delete(
            synchronize_session=False
        )
        self.session.flush()


    def is_email_taken(
        self, 
        email: str, 
        customer_id: Optional[str] = None
    ) -> bool:
        """
        Checks if an email is already taken by another customer in the Employee MySQL database.

        :param email: The email to check.
        :type email: str
        :param customer_id: The ID of the customer to exclude from the check (optional).
        :type customer_id: str | None
        :return: True if the email is already taken, False otherwise.
        :rtype: bool
        """
        customer_query = self.session.query(CustomerEntity).filter_by(email=email)
        if customer_id is not None and isinstance(customer_id, str):
            customer_query = customer_query.filter(CustomerEntity.id != customer_id)
        return customer_query.first() is not None
