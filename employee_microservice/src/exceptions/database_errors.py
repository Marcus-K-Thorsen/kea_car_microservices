from typing import Union
from uuid import UUID
from datetime import date

from src.entities import ModelEntity, ColorEntity, CarEntity

class DatabaseError(Exception):
    pass


class AlreadyTakenFieldValueError(DatabaseError):
    def __init__(self, entity_name: str, field: str, value: str):
        self.message = f'{entity_name} with {field}: {value} is already taken.'
        super().__init__(self.message)  # Call the base class constructor

    def __str__(self):
        return f"{self.message}"

class FileTooLargeError(DatabaseError):
    def __init__(self, file_name: str, max_mega_bytes_size: int):
        self.message = f'The file: {file_name} is too large. Maximum allowed size is {max_mega_bytes_size}MB.'
        super().__init__(self.message)  # Initialize the base Exception with the message

    def __str__(self):
        return f"{self.message}"


class FileIsNotCorrectFileTypeError(DatabaseError):
    def __init__(self, file_name: str, file_type: str, allowed_file_types: list[str]):
        self.message = (f'The file: {file_name} is a {file_type} file. '
                        f'Allowed file types are: {", ".join(allowed_file_types)}.')
        super().__init__(self.message)  # Initialize the base Exception with the message

    def __str__(self):
        return f"{self.message}"


class FileCannotBeEmptyError(DatabaseError):
    def __init__(self):
        self.message = "Filename cannot be empty."
        super().__init__(self.message)  # Initialize the base Exception with the message

    def __str__(self):
        return f"{self.message}"

class UnableToFindIdError(DatabaseError):
    def __init__(self, entity_name: str, entity_id: Union[str, UUID]):
        entity_id= str(entity_id) if isinstance(entity_id, UUID) else entity_id
        self.message = f'{entity_name} with ID: {entity_id} does not exist.'
        super().__init__(self.message)  # Initialize the base Exception with the message

    def __str__(self):
        return f"{self.message}"

class UnableToUndeleteAlreadyUndeletedEntityError(DatabaseError):
    def __init__(self, entity_name: str, entity_id: Union[str, UUID]):
        entity_id= str(entity_id) if isinstance(entity_id, UUID) else entity_id
        self.message = f'{entity_name} with ID: {entity_id} has not been deleted yet and can not be undeleted.'
        super().__init__(self.message)  # Initialize the base Exception with the message

    def __str__(self):
        return f"{self.message}"

class UnableToDeleteAlreadyDeletedEntityError(DatabaseError):
    def __init__(self, entity_name: str, entity_id: Union[str, UUID]):
        entity_id= str(entity_id) if isinstance(entity_id, UUID) else entity_id
        self.message = f'{entity_name} with ID: {entity_id} has already been deleted and can not be deleted again.'
        super().__init__(self.message)  # Initialize the base Exception with the message

    def __str__(self):
        return f"{self.message}"


class TheColorIsNotAvailableInModelToGiveToCarError(DatabaseError):
    def __init__(self, model: ModelEntity, color: ColorEntity):
        self.message = (f'The model: {model.name} with colors: '
                        f'{[color.name for color in model.colors]} does not have the color: '
                        f'{color.name} to be given to a car.')
        super().__init__(self.message)  # Call the base class constructor

    def __str__(self):
        return f"{self.message}"
    
    
class UnableToDeleteCarWithoutDeletingPurchaseTooError(DatabaseError):
    def __init__(self, car: CarEntity):
        self.message = f"The car with ID: '{car.id}' must delete its purchase too."
        super().__init__(self.message)  # Call the base class constructor

    def __str__(self):
        return f"{self.message}"


class PurchaseDeadlineHasPastError(DatabaseError):
    def __init__(self, car: CarEntity, date_of_purchase: date):
        self.message = (f'Car with ID: {car.id} has a Purchase Deadline: '
                        f'{car.purchase_deadline.strftime("%d-%m-%Y")} that has past the date of purchase: '
                        f'{date_of_purchase.strftime("%d-%m-%Y")}.')
        super().__init__(self.message)  # Initialize the base Exception with the message

    def __str__(self):
        return f"{self.message}"
    

class UnableToFindEntityError(DatabaseError):
    def __init__(self, entity_name: str, field: str, value: str):
        self.message = f'{entity_name} with {field}: {value} does not exist.'
        super().__init__(self.message)  # Call the base class constructor

    def __str__(self):
        return f"{self.message}"