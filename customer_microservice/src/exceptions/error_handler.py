# External Library imports
from typing import Callable
import logging

from fastapi import HTTPException, status

# Internal library imports
from src.exceptions.database_exceptions import UnableToFindIdError


"""
# Description:
The error handler will a callback function from a given service and catch any 
exceptions and raise an HTTPException with the appropriate status code and message.


# Usage example:
```
return handle_http_exception(
    error_message="Failed to get colors from the Customer database",
    callback=lambda: service.get_all(
        database=customer_database, 
        colors_limit=limit
        )
    )
```
"""
def handle_http_exception(error_message: str, callback: Callable):
    try:
        return callback()

    except UnableToFindIdError as e:
        log_error(error_message, e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
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
    logging.error(f"{error.__class__.__name__} Was Caught.\n{error_message}:\n{error}", exc_info=True)
