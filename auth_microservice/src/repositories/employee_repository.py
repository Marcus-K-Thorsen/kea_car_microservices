# External Library imports
from typing import Optional

# Internal library imports
from src.entities import EmployeeEntity
from src.repositories.base_repository import BaseRepository


class EmployeeRepository(BaseRepository):
    def get_by_id(self, employee_id: str) -> Optional[EmployeeEntity]:
        """
        Retrieves an employee by ID from the Auth Mongo database.
        
        :param employee_id: The ID of the employee to retrieve.
        :type employee_id: str
        :return: The employee if found, None otherwise.
        :rtype: EmployeeEntity | None
        """
        employees_collection = self.get_employees_collection()
        employee_query = employees_collection.find_one(
            {"_id": employee_id}
        )
        
        if employee_query is not None:
            return EmployeeEntity(**employee_query)
        
        return None
    
    
    def get_by_email(self, email: str) -> Optional[EmployeeEntity]:
        """
        Retrieves an employee by email from the Auth Mongo database.
        
        :param email: The email of the employee to retrieve.
        :type email: str
        :return: The employee if found, None otherwise.
        :rtype: EmployeeEntity | None
        """
        employees_collection = self.get_employees_collection()
        employee_query = employees_collection.find_one(
            {"email": email}
        )
        
        if employee_query is not None:
            return EmployeeEntity(**employee_query)
        
        return None
    
    
    def create(self, employee: EmployeeEntity) -> EmployeeEntity:
        """
        Creates a new employee in the Auth Mongo database.
        This function is only to be used for consuming messages from the queue.
        It is not to be used for creating employees from the API.
        
        :param employee: The employee to create.
        :type employee: EmployeeEntity
        :return: The created employee.
        :rtype: EmployeeEntity
        """
        employees_collection = self.get_employees_collection()
        employees_collection.insert_one(employee.to_mongo_dict(exlude_id=False))
        
        return employee
    
    
    def update(self, employee: EmployeeEntity) -> Optional[EmployeeEntity]:
        """
        Updates an employee in the Auth Mongo database.
        This function is only to be used for consuming messages from the queue.
        It is not to be used for updating employees from the API.
        
        :param employee: The employee to update.
        :type employee: EmployeeEntity
        :return: The updated employee if successful, None otherwise.
        :rtype: EmployeeEntity | None
        """
        employees_collection = self.get_employees_collection()
        updated_employee = employees_collection.find_one_and_update(
            {"_id": employee.id},
            {"$set": employee.to_mongo_dict(exlude_id=True)},
            return_document=True
        )
        
        if updated_employee is not None:
            return employee
        
        return None


    def delete(self, employee_id: str) -> bool:
        """
        Deletes an employee by ID in the Employee Mongo database.
        This function is only to be used for consuming messages from the queue.
        It is not to be used for deleting employees from the API.
        
        :param employee_id: The ID of the employee to delete.
        :type employee_id: str
        :return: True if the employee was deleted, False otherwise.
        :rtype: bool
        """
        employees_collection = self.get_employees_collection()
        result = employees_collection.delete_one({"_id": employee_id})
        
        return result.deleted_count > 0
    
    
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
        employee_query = {"email": email}
        if employee_id is not None and isinstance(employee_id, str):
            employee_query["_id"] = {"$ne": employee_id}
        return self.get_employees_collection().count_documents(employee_query) > 0
