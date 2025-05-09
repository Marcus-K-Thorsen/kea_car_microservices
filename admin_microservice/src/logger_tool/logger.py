import logging
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def log_and_raise_error(message: str, logger_level: str = "warning", exception_type: Optional[Exception] = None) -> None:
    """
    Logs a message at the specified logging level and raises an exception with the same message.

    Args:
        message (str): The message to log and include in the raised exception.
                      Example: "The given email is invalid."
        logger_level (str): The logging level to use. Options are:
                            - "warning" (default)
                            - "error"
                            - "info"
                            - "debug"
                            Example: "error"
        exception_type (Optional[Exception]): The type of exception to raise. If not provided, a ValueError is raised by default.
                                              Example: KeyError, RuntimeError, or any custom exception class.

    Raises:
        ValueError: If no exception_type is provided, a ValueError is raised with the given message.
        exception_type: If an exception_type is provided, it is raised with the given message.

    Usage Examples:
        >>> log_and_raise_error("The given email is invalid.")
        Logs: "The given email is invalid." at the "warning" level.
        Raises: ValueError("The given email is invalid.")

        >>> log_and_raise_error("The given password is too short.", logger_level="error", exception_type=RuntimeError)
        Logs: "The given password is too short." at the "error" level.
        Raises: RuntimeError("The given password is too short.")
    """
    if logger_level == "warning":
        logger.warning(message)
    elif logger_level == "error":
        logger.error(message)
    elif logger_level == "info":
        logger.info(message)
    else:
        logger.debug(message)
    
    if exception_type:
        raise exception_type(message)
    else:
        raise ValueError(message)