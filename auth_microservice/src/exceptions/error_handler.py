# External Library imports
from typing import Callable
from fastapi import HTTPException, status


# Internal library imports
from src.logger_tool import logger
from src.exceptions.invalid_credentials_errors import IncorrectCredentialError



def handle_http_exception(error_message: str, callback: Callable):
    try:
        return callback()

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


