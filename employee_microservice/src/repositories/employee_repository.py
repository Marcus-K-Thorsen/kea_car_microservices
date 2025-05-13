# External Library imports
from typing import Optional

# Internal library imports
from src.entities import EmployeeEntity, EmployeeMesssage
from src.repositories.base_repository import BaseRepository


class EmployeeRepository(BaseRepository):
    def get_all(self, limit: Optional[int] = None) -> list[EmployeeEntity]:
        """
        Retrieves all employees from the database.
        
        :param limit: The maximum number of employees to retrieve (optional).
        :type limit: int | None
        :return: A list of EmployeeEntity objects.
        :rtype: list[EmployeeEntity]
        """
        employees_query = self.session.query(EmployeeEntity)
        
        if self.limit_is_valid(limit):
            employees_query = employees_query.limit(limit)
        
        return employees_query.all()
    
    def get_by_id(self, employee_id: str) -> Optional[EmployeeEntity]:
        """
        Retrieves an employee by ID.
        
        :param employee_id: The ID of the employee to retrieve.
        :type employee_id: str
        :return: The employee if found, None otherwise.
        :rtype: EmployeeEntity | None
        """
        return self.session.get(EmployeeEntity, employee_id)
    
    
    def get_by_email(self, email: str) -> Optional[EmployeeEntity]:
        """
        Retrieves an employee by email.
        
        :param email: The email of the employee to retrieve.
        :type email: str
        :return: The employee if found, None otherwise.
        :rtype: EmployeeEntity | None
        """
        return self.session.query(EmployeeEntity).filter_by(email=email).first()
    
    
    def create(self, employee: EmployeeMesssage) -> EmployeeEntity:
        """
        Creates a new employee in the database.
        
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
            created_at=employee.created_at,
            updated_at=employee.updated_at
        )
        self.session.add(new_employee)
        self.session.flush()
        self.session.refresh(new_employee)
        
        return employee
    
    
    def update(self, employee: EmployeeMesssage) -> Optional[EmployeeEntity]:
        """
        Updates an employee in the database.
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


    def delete(self, employee: EmployeeMesssage) -> EmployeeEntity:
        """
        Deletes an employee by ID.
        
        :param employee: The employee to delete.
        :type employee: EmployeeMesssage
        :return: The Employee that was just deleted, but with the 'is_deleted' set to True
        :rtype: EmployeeEntity
        """
        existing_employee = self.get_by_id(employee.id)
        if employee is None:
            return None
        
        setattr(existing_employee, "is_deleted", True)
        setattr(existing_employee, "updated_at", employee.updated_at)
        self.session.flush()
        self.session.refresh(existing_employee)
        return existing_employee
    
    
    def is_email_taken(
        self, 
        email: str, 
        employee_id: Optional[str] = None
    ) -> bool:
        """
        Checks if an email is already taken by another employee.

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
        
