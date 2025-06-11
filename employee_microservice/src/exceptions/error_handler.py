# External Library imports
from typing import Callable
from fastapi import HTTPException, status


# Internal library imports
from src.logger_tool import logger
from src.exceptions.invalid_credentials_errors import (
    IncorrectCredentialError,
    IncorrectRoleError,
    CurrentEmployeeDeletedError,
    UnableToDeleteAnotherEmployeesCarError,
    EmployeeIsNotAllowedToRetrieveOrMakeCarPurchasesBasedOnOtherEmployeeError
    )
from src.exceptions.database_errors import (
    FileTooLargeError,
    UnableToFindIdError,
    FileCannotBeEmptyError,
    UnableToFindEntityError,
    FileIsNotCorrectFileTypeError,
    AlreadyTakenFieldValueError,
    PurchaseDeadlineHasPastError,
    TheColorIsNotAvailableInModelToGiveToCarError,
    UnableToDeleteCarWithoutDeletingPurchaseTooError,
)



def handle_http_exception(error_message: str, callback: Callable):
    try:
        return callback()

    except UnableToFindIdError as e:
        log_error(error_message, e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(f"{error_message}: {e}")
        )
        
    except UnableToFindEntityError as e:
        log_error(error_message, e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(f"{error_message}: {e}")
        )
        
    except PurchaseDeadlineHasPastError as e:
        log_error(error_message, e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(f"{error_message}: {e}")
        )
        
    except AlreadyTakenFieldValueError as e:
        log_error(error_message, e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(f"{error_message}: {e}")
        )
        
    except CurrentEmployeeDeletedError as e:
        log_error(error_message, e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(f"{error_message}: {e}")
        )
        
    except IncorrectRoleError as e:
        log_error(error_message, e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(f"{error_message}: {e}")
        )
    
    except UnableToDeleteAnotherEmployeesCarError as e:
        log_error(error_message, e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(f"{error_message}: {e}")
        )
        
    except TheColorIsNotAvailableInModelToGiveToCarError as e:
        log_error(error_message, e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(f"{error_message}: {e}")
        )
        
    except UnableToDeleteCarWithoutDeletingPurchaseTooError as e:
        log_error(error_message, e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(f"{error_message}: {e}")
        )
        
    except FileCannotBeEmptyError as e:
        log_error(error_message, e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(f"{error_message}: {e}")
        )
        
    except FileTooLargeError as e:
        log_error(error_message, e)
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=str(f"{error_message}: {e}")
        )
        
    except FileIsNotCorrectFileTypeError as e:
        log_error(error_message, e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(f"{error_message}: {e}")
        )
        
    except EmployeeIsNotAllowedToRetrieveOrMakeCarPurchasesBasedOnOtherEmployeeError as e:
        log_error(error_message, e)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(f"{error_message}: {e}")
        )
        
    except IncorrectCredentialError as e:
        log_error(error_message, e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(f"{error_message}: {e}")
        )

    except Exception as e:
        log_error(error_message, e)
        # Raise a generic internal server error for the client
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(f"Internal Server Error Caught: {error_message}.")
        )

def log_error(error_message: str, error: Exception):  # pragma: no cover
    # Log internal server errors for debugging
    logger.error(f"{error.__class__.__name__} Was Caught.\n{error_message}:\n{error}", exc_info=True)


