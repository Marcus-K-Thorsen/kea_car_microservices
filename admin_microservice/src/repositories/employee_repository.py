# External Library imports
from sqlalchemy import text
from typing import Optional, List

# Internal library imports
from src.resources import EmployeeCreateResource, EmployeeUpdateResource
from src.repositories.base_repository import BaseRepository
from src.entities import EmployeeEntity


class EmployeeRepository(BaseRepository):
    
    def get_all(
        self, 
        limit: Optional[int] = None, 
        deletion_filter: Optional[bool] = None
    ) -> List[EmployeeEntity]:
        """
        Retrieves a list of employees from the Admin MySQL database.

        :param limit: The maximum number of employees to retrieve (optional).
        :type limit: int | None
        :param deletion_filter: Filter for deleted employees.
        
                                - `None` (default behavior): Only active employees.
                                - `True`: Only deleted employees.
                                - `False`: Both active and deleted employees.
        :type deletion_filter: bool | None
        :return: A list of employees.
        :rtype: List[EmployeeEntity]
        """
        employee_query = self.session.query(EmployeeEntity)

        # Apply the `deletion_filter` logic
        if deletion_filter is None:
            # Default behavior: Only return employees that are not deleted
            employee_query = employee_query.filter(EmployeeEntity.is_deleted == False)
        elif deletion_filter is True:
            # Return only deleted employees
            employee_query = employee_query.filter(EmployeeEntity.is_deleted == True)

        # Apply the limit if provided
        if self.limit_is_valid(limit):
            employee_query = employee_query.limit(limit)

        return employee_query.all()
    
    
    def get_by_id(self, employee_id: str) -> Optional[EmployeeEntity]:
        """
        Retrieves an employee by their ID from the Admin MySQL database.

        :param employee_id: The ID of the employee to retrieve.
        :type employee_id: str
        :return: The `EmployeeEntity` object if found, otherwise None.
        :rtype: EmployeeEntity | None
        """
        return self.session.get(EmployeeEntity, employee_id)
    
    
    def get_by_email(self, email: str) -> Optional[EmployeeEntity]:
        """
        Retrieves an employee by their email from the Admin MySQL database.

        :param email: The email of the employee to retrieve.
        :type email: str
        :return: The `EmployeeEntity` object if found, otherwise None.
        :rtype: EmployeeEntity | None
        """
        return self.session.query(EmployeeEntity).filter_by(email=email).first()
    
        
    def create(
        self, 
        employee_create_data: EmployeeCreateResource,
        hashed_password: str
    ) -> EmployeeEntity:
        """
        Creates a new employee record in the Admin MySQL database.

        :param employee_create_data: The employee data to be created.
        :type employee_create_data: EmployeeCreateResource
        :return: The created `EmployeeEntity` object.
        :rtype: EmployeeEntity
        """
        
        
        # Create a new employee entity
        new_employee = EmployeeEntity(
            id=str(employee_create_data.id),
            email=str(employee_create_data.email),
            hashed_password=hashed_password,
            first_name=employee_create_data.first_name,
            last_name=employee_create_data.last_name,
            role=employee_create_data.role,
            is_deleted=False,
        )
        
        # Add the new employee to the session and commit
        self.session.add(new_employee)
        self.session.flush()  # Ensure the new employee is added to the session
        self.session.refresh(new_employee)
        
        return new_employee
    
    
    def update(
        self, 
        employee_id: str, 
        employee_update_data: EmployeeUpdateResource,
        hashed_password: Optional[str] = None
    ) -> Optional[EmployeeEntity]:
        """
        Updates an existing employee record in the Admin MySQL database.

        :param employee_id: The ID of the employee to update.
        :type employee_id: str
        :param employee_update_data: The updated employee data.
        :type employee_update_data: EmployeeUpdateResource
        :return: The updated `EmployeeEntity` object if found, otherwise None.
        :rtype: EmployeeEntity | None
        """
        # Retrieve the existing employee entity
        employee = self.get_by_id(employee_id)
        
        if not employee:
            return None
        
        # Update the fields of the existing employee entity
        for field, value in employee_update_data.get_updated_fields().items():
            if field == "password":
                continue
            if field == "email":
                value = str(value)
            setattr(employee, field, value)
            
        if hashed_password is not None and isinstance(hashed_password, str):
            employee.hashed_password = hashed_password
        
        self.session.flush()
        self.session.refresh(employee)
        
        return employee
    
    
    def __update_deletion_status(
        self, 
        is_set_to_be_deleted: bool, 
        employee_to_update: EmployeeEntity
    ) -> EmployeeEntity:
        """
        Updates the deletion status of an employee in the Admin MySQL database.

        This function can mark an employee as deleted (`is_deleted=True`) or undelete an employee (`is_deleted=False`).

        :param is_set_to_be_deleted: Indicates whether the employee should be marked as deleted.
        :type is_set_to_be_deleted: bool
        :param employee_to_update: The employee entity to update.
        :type employee_to_update: EmployeeEntity
        :return: The updated `EmployeeEntity` object.
        :rtype: EmployeeEntity
        """
        # Use a raw SQL query to update only the `is_deleted` field and preserve `updated_at`
        self.session.execute(
            text("""
                UPDATE employees
                SET is_deleted = :deletion_status, updated_at = :current_updated_at
                WHERE id = :id
            """),
            {
                "deletion_status": is_set_to_be_deleted,
                "current_updated_at": employee_to_update.updated_at,
                "id": employee_to_update.id
            }
        )
        self.session.flush()
        self.session.refresh(employee_to_update)

        return employee_to_update
    
    
    def delete(self, employee_to_delete: EmployeeEntity) -> EmployeeEntity:
        """
        Marks an employee as deleted in the Admin MySQL database.

        :param employee_to_delete: The employee entity to mark as deleted.
        :type employee_to_delete: EmployeeEntity
        :return: The updated `EmployeeEntity` object that is now set to have been deleted.
        :rtype: EmployeeEntity
        """
        return self.__update_deletion_status(
            is_set_to_be_deleted=True, 
            employee_to_update=employee_to_delete
            )
    
    
    def undelete(self, employee_to_undelete: EmployeeEntity) -> EmployeeEntity:
        """
        Undeletes an employee in the Admin MySQL database.

        :param employee_to_undelete: The employee entity to undelete.
        :type employee_to_undelete: EmployeeEntity
        :return: The updated `EmployeeEntity` object that is now set to have been undeleted/activated.
        :rtype: EmployeeEntity
        """
        return self.__update_deletion_status(
            is_set_to_be_deleted=False, 
            employee_to_update=employee_to_undelete
            )
    
    
    def is_email_taken(
        self, 
        email: str, 
        employee_id: Optional[str] = None
    ) -> bool:
        """
        Checks if an email is already taken by another employee in the Admin MySQL database.

        :param email: The email to check.
        :type email: str
        :param employee_id: The ID of the employee to exclude from the check (optional).
        :type employee_id: str | None
        :return: True if the email is already taken, False otherwise.
        :rtype: bool
        """
        employee_query = self.session.query(EmployeeEntity).filter_by(email=email)
        if employee_id is not None and isinstance(employee_id, str):
            employee_query = employee_query.filter(EmployeeEntity.id != employee_id)
        return employee_query.first() is not None

