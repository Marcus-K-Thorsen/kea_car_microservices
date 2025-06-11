from .error_handler import handle_http_exception

from .database_errors import (
    UnableToDeleteCarWithoutDeletingPurchaseTooError,
    TheColorIsNotAvailableInModelToGiveToCarError,
    UnableToUndeleteAlreadyUndeletedEntityError,
    UnableToDeleteAlreadyDeletedEntityError,
    PurchaseDeadlineHasPastError,
    FileIsNotCorrectFileTypeError,
    AlreadyTakenFieldValueError,
    UnableToFindEntityError,
    FileCannotBeEmptyError,
    UnableToFindIdError,
    FileTooLargeError
)

from .invalid_credentials_errors import (
    IncorrectCredentialError,
    IncorrectIdError,
    IncorrectRoleError,
    CurrentEmployeeDeletedError,
    UnableToDeleteAnotherEmployeesCarError,
    EmployeeIsNotAllowedToRetrieveOrMakeCarPurchasesBasedOnOtherEmployeeError
)