# External Library imports
from typing import Optional, List

# Internal library imports
from src.entities import EmployeeEntity, EmployeeMesssage
from src.repositories.base_repository import BaseRepository


class EmployeeRepository(BaseRepository):
    def get_all(
        self, 
        limit: Optional[int] = None, 
        deletion_filter: Optional[bool] = None
    ) -> List[EmployeeEntity]:
        """
        Retrieves a list of employees from the Employee MySQL database.

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
        Retrieves an employee by ID from the Employee MySQL database.
        
        :param employee_id: The ID of the employee to retrieve.
        :type employee_id: str
        :return: The employee if found, None otherwise.
        :rtype: EmployeeEntity | None
        """
        return self.session.get(EmployeeEntity, employee_id)
    
    
    def get_by_email(self, email: str) -> Optional[EmployeeEntity]:
        """
        Retrieves an employee by email from the Employee MySQL database.
        
        :param email: The email of the employee to retrieve.
        :type email: str
        :return: The employee if found, None otherwise.
        :rtype: EmployeeEntity | None
        """
        return self.session.query(EmployeeEntity).filter_by(email=email).first()
    
    
    def create(self, employee: EmployeeMesssage) -> EmployeeEntity:
        """
        Creates a new employee in the Employee MySQL database.
        This function is only to be used for consuming messages from the queue.
        It is not to be used for creating employees from the API.
        
        :param employee: The employee to create.
        :type employee: EmployeeMesssage
        :return: The created employee.
        :rtype: EmployeeEntity
        """
        new_employee = EmployeeEntity(
            id=employee.id,
            first_name=employee.first_name,
            last_name=employee.last_name,
            email=employee.email,
            hashed_password=employee.hashed_password,
            role=employee.role,
            is_deleted=employee.is_deleted,
            created_at=employee.created_at,
            updated_at=employee.updated_at
        )
        self.session.add(new_employee)
        self.session.flush()
        self.session.refresh(new_employee)
        
        return employee
    
    
    def update(self, employee: EmployeeMesssage) -> Optional[EmployeeEntity]:
        """
        Updates an employee in the Employee MySQL database.
        This function is only to be used for consuming messages from the queue.
        It is not to be used for updating employees from the API.
        
        :param employee: The employee to update.
        :type employee: EmployeeMesssage
        :return: The updated employee if successful, None otherwise.
        :rtype: EmployeeEntity | None
        """
        existing_employee = self.get_by_id(employee.id)
        if existing_employee is None:
            return None
        
        for key, value in employee.model_dump(exclude_unset=True).items():
            if key != "id":
                # Update the existing employee's attributes
                setattr(existing_employee, key, value)
        
        self.session.flush()
        self.session.refresh(existing_employee)
        return existing_employee


    def delete(self, employee: EmployeeEntity) -> EmployeeEntity:
        """
        Deletes an employee from the Employee MySQL database, by setting its is_deleted value to True.
        This is a soft delete, meaning the employee is not actually removed from the database,
        but marked as deleted. And the updated_at value is not updated.
        This function is only to be used for consuming messages from the queue.
        It is not to be used for deleting employees from the API.
        
        :param employee: The employee from the database to delete.
        :type employee: EmployeeEntity
        :return: The Employee that was just deleted, but with its is_deleted set to True.
        :rtype: EmployeeEntity
        """
        self.session.query(EmployeeEntity).filter_by(id=employee.id).update(
            {"is_deleted": True, "updated_at": employee.updated_at}, synchronize_session=False
        )
        self.session.flush()
        self.session.refresh(employee)
        return employee
    
    
    def undelete(self, employee: EmployeeEntity) -> EmployeeEntity:
        """
        Undeletes an employee from the Employee MySQL database, by setting its is_deleted value to False.
        This is a soft undelete, meaning the employee is not actually restored from the database,
        but marked as undeleted. And the updated_at value is not updated.
        This function is only to be used for consuming messages from the queue.
        It is not to be used for undeleting employees from the API.
        
        :param employee: The employee from the database to undelete.
        :type employee: EmployeeEntity
        :return: The Employee that was just undeleted, but with its is_deleted set to False.
        :rtype: EmployeeEntity
        """
        self.session.query(EmployeeEntity).filter_by(id=employee.id).update(
            {"is_deleted": False, "updated_at": employee.updated_at}, synchronize_session=False
        )
        self.session.flush()
        self.session.refresh(employee)
        return employee
    
    
    def is_email_taken(
        self, 
        email: str, 
        employee_id: Optional[str] = None
    ) -> bool:
        """
        Checks if an email is already taken by another employee in the Employe MySQL database.

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
        
