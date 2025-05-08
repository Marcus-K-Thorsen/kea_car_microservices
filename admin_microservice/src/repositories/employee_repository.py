# External Library imports
from typing import Optional, List

# Internal library imports
from src.resources import EmployeeCreateResource, EmployeeUpdateResource
from src.repositories.base_repository import BaseRepository
from src.entities import EmployeeEntity
from src.core import get_password_hash


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
    
        
    def create(self, employee_create_data: EmployeeCreateResource) -> EmployeeEntity:
        """
        Creates a new employee record in the Admin MySQL database.

        :param employee_create_data: The employee data to be created.
        :type employee_create_data: EmployeeCreateResource
        :return: The created `EmployeeEntity` object.
        :rtype: EmployeeEntity
        """
        # Hash the password before storing it
        hashed_password = get_password_hash(employee_create_data.password)
        
        # Create a new employee entity
        new_employee = EmployeeEntity(
            id=employee_create_data.id,
            email=employee_create_data.email,
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
    
    def is_email_taken(self, email: str) -> bool:
        """
        Checks if an email is already taken by another employee.

        :param email: The email to check.
        :type email: str
        :return: True if the email is taken, False otherwise.
        :rtype: bool
        """
        return self.session.query(EmployeeEntity).filter_by(email=email).first() is not None

