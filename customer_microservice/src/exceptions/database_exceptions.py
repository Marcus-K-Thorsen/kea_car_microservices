"""
**Database Exceptions Module**

This module defines custom exceptions related to database operations. These exceptions
are used to handle errors when interacting with the database, such as when an entity
with a specific ID cannot be found.

Key Responsibilities:

- Provide a base exception class for database-related errors (`DatabaseError`).
- Define a specific exception for missing entities (`UnableToFindIdError`).
"""

from typing import Union
from uuid import UUID


class DatabaseError(Exception):
    """
    Base exception class for database-related errors.

    This class serves as the foundation for all custom exceptions related to database
    operations in the system.
    """
    pass


class UnableToFindIdError(DatabaseError):
    """
    Exception raised when an entity with a specific ID cannot be found in the database.

    This exception is used to indicate that a requested entity does not exist in the
    database. It provides a detailed error message that includes the entity name and ID.

    Attributes:
        entity_name (str): The name of the entity that could not be found.
        entity_id (Union[str, UUID]): The ID of the entity that could not be found.
        message (str): A detailed error message describing the issue.
    """

    def __init__(self, entity_name: str, entity_id: Union[str, UUID]):
        """
        Initializes the `UnableToFindIdError` exception.

        :param entity_name: The name of the entity that could not be found.
        :type entity_name: str
        :param entity_id: The ID of the entity that could not be found.
        :type entity_id: Union[str, UUID]
        """
        entity_id = str(entity_id) if isinstance(entity_id, UUID) else entity_id
        self.message = f'{entity_name} with ID: {entity_id} does not exist.'
        super().__init__(self.message)  # Initialize the base Exception with the message

    def __str__(self):
        """
        Returns the string representation of the exception.

        :return: The error message.
        :rtype: str
        """
        return f"{self.message}"
