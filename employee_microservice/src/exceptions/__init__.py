from .error_handler import handle_http_exception

from .database_errors import (
    UnableToDeleteCarWithoutDeletingPurchaseTooError,
    TheColorIsNotAvailableInModelToGiveToCarError,
    UnableToUndeleteAlreadyUndeletedEntityError,
    UnableToDeleteAlreadyDeletedEntityError,
    PurchaseDeadlineHasPastError,
    AlreadyTakenFieldValueError,
    UnableToFindEntityError,
    UnableToFindIdError
)

from .invalid_credentials_errors import (
    IncorrectCredentialError,
    IncorrectIdError,
    IncorrectRoleError,
    CurrentEmployeeDeletedError,
    UnableToDeleteAnotherEmployeesCarError,
    EmployeeIsNotAllowedToRetrieveOrMakeCarPurchasesBasedOnOtherEmployeeError
)