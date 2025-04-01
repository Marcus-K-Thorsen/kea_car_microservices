"""
**Error Handler Module**

This module provides utility functions to handle exceptions raised during service operations
and convert them into appropriate HTTP responses for FastAPI endpoints.

Key Responsibilities:

- Catch and handle exceptions raised by service functions.
- Log errors for debugging purposes.
- Raise HTTP exceptions with appropriate status codes and error messages.
"""

# External Library imports
from typing import Callable
import logging

from fastapi import HTTPException, status

# Internal library imports
from src.exceptions.database_exceptions import UnableToFindIdError


def handle_http_exception(error_message: str, callback: Callable):
    """
    Handles exceptions raised by a service function and converts them into HTTP exceptions.

    This function executes a callback function (typically a service operation) and catches
    any exceptions raised during its execution. It logs the error and raises an appropriate
    HTTP exception for the client.

    :param error_message: A descriptive error message to include in the HTTP exception.
    :type error_message: str
    :param callback: A callable function (e.g., a service operation) to execute.
    :type callback: Callable
    :return: The result of the callback function if no exceptions are raised.
    :raises HTTPException: If an exception is caught, an HTTP exception is raised with the
                           appropriate status code and error message.
    """
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


def log_error(error_message: str, error: Exception):
    """
    Logs an error message and exception details for debugging purposes.

    This function logs the error class, message, and stack trace to help with debugging
    internal server errors.

    :param error_message: A descriptive error message to log.
    :type error_message: str
    :param error: The exception object to log.
    :type error: Exception
    """
    logging.error(f"{error.__class__.__name__} Was Caught.\n{error_message}:\n{error}", exc_info=True)
