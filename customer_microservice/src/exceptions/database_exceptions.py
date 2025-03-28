from datetime import date
from typing import Union
from uuid import UUID


class DatabaseError(Exception):
    pass


class UnableToFindIdError(DatabaseError):
    def __init__(self, entity_name: str, entity_id: Union[str, UUID]):
        entity_id= str(entity_id) if isinstance(entity_id, UUID) else entity_id
        self.message = f'{entity_name} with ID: {entity_id} does not exist.'
        super().__init__(self.message)  # Initialize the base Exception with the message

    def __str__(self):
        return f"{self.message}"

