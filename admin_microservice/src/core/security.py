# External Library imports
import hashlib
import requests
from typing import Union, List
from datetime import datetime, timezone
from fastapi import Depends, HTTPException, status
from jwt import ExpiredSignatureError, InvalidTokenError, decode

# Internal Library imports
from src.repositories import EmployeeRepository
from src.database_management import Session
from src.entities import EmployeeEntity
from src.resources import RoleEnum
from src.core.tokens import TokenPayload
from src.logger_tool import log_and_raise_error, logger
from src.exceptions import (
    IncorrectIdError, 
    CurrentEmployeeDeletedError,
    IncorrectRoleError
)
from src.core.config import (
    pwd_context,
    SECRET_KEY,
    ALGORITHM,
    oauth2
)

def get_current_employee(
    token_payload: TokenPayload, 
    session: Session,
    current_user_action: str,
    valid_roles: Union[RoleEnum, List[RoleEnum], None] = None
) -> EmployeeEntity:
    """
    Retrieves the current employee from the database using the provided token payload and checks if it is a valid employee.

    Args:
        token_payload (TokenPayload): The payload containing the token information, such as the ID for the current employee.
        session (Session): The database session to access employee data.
        current_user_action (str): The action the current user is about to perform.
        valid_roles (RoleEnum | List[RoleEnum] | None): The valid roles for the current employee.
            If None, no role validation is performed. If provided, the current employee's role must match one of the valid roles.

    Returns:
        EmployeeEntity: The current employee entity.

    Raises:
        TypeError: If the token_payload is not of type TokenPayload or session is not of type Session or if the current_user_action is not of type string, or if the valid_roles is not of type RoleEnum, List[RoleEnom] or None.
        ValueError: If the current_user_action is an empty string.
        IncorrectEmailError: If the employee with the given email is not found in the database.
        CurrentEmployeeDeletedError: If the current employee is marked as deleted in the database.
        IncorrectRoleError: If the current employee's role does not match the valid roles provided.
    """
    if not isinstance(token_payload, TokenPayload):
        raise TypeError(f"token_payload must be of type TokenPayload, "
                        f"not {type(token_payload).__name__}.")
    if not isinstance(session, Session):
        raise TypeError(f"session must be of type Session, "
                        f"not {type(session).__name__}.")
    if not isinstance(current_user_action, str):
        raise TypeError(f"current_user_action must be of type str, "
                        f"not {type(current_user_action).__name__}.")
    current_user_action = current_user_action.strip()
    if len(current_user_action) == 0:
        raise ValueError("current_user_action must be a non-empty string.")
    
    if valid_roles is not None and not (
        isinstance(valid_roles, RoleEnum) or
        (isinstance(valid_roles, list) and all(isinstance(role, RoleEnum) for role in valid_roles))
    ):
        raise TypeError(f"valid_roles must be of type RoleEnum, List[RoleEnum], or None, "
                        f"not {type(valid_roles).__name__}.")
    
    current_employee = EmployeeRepository(session).get_by_id(token_payload.employee_id)
    
    if current_employee is None:
        raise IncorrectIdError(token_payload.employee_id)
    
    if current_employee.is_deleted:
        raise CurrentEmployeeDeletedError(current_employee)
    
    if valid_roles is not None:
        if current_employee.role not in valid_roles:
            raise IncorrectRoleError(
                email_of_current_employee=current_employee.email,
                incorrect_role=current_employee.role,
                correct_roles=valid_roles,
                action=current_user_action
            )
    
    return current_employee
    

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def is_password_to_short(password: str) -> bool:
    """
    Checks if the given password is too short.

    The password is considered too short if its length is less than 8 characters.

    Args:
        password (str): The password to check.

    Returns:
        bool: True if the password is too short, False otherwise.
    """
    return len(password) < 8


def is_password_pwned(password: str) -> bool:
    """
    Checks if the given password has been exposed in a known data breach.

    This function uses an online service called "Have I Been Pwned" to check if the password
    has been leaked in any past data breaches. To protect your privacy, the full password is
    never sent to the service. Instead, the password is converted into a secure code (called a hash),
    and only a small part of that code is sent to the service. The service then returns a list of
    possible matches, and the function checks if your password is among them.

    If the password has been found in a breach, it is considered unsafe to use.

    Args:
        password (str): The password to check.

    Raises:
        RuntimeError: If there is an issue connecting to the online service.

    Returns:
        bool: True if the password has been found in a breach, False otherwise.
    """
    # Hash the password using SHA-1 and convert it to uppercase
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    
    # Split the hash into a prefix (first 5 characters) and suffix (remaining 35 characters)
    prefix, suffix = sha1_password[:5], sha1_password[5:]
    
    # Query the Have I Been Pwned API with the prefix
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)
    
    # Raise an error if the API request fails
    if not response.ok:
        log_and_raise_error(f"Error querying the Have I Been Pwned API at URL: '{url}', " 
                            f"with the sha1_password: '{sha1_password}'.",
                            logger_level="error", 
                            exception_type=RuntimeError)
    
    # Check if the suffix is in the list of hashes returned by the API
    hashes = (line.split(':') for line in response.text.splitlines())
    return any(suffix == h for h, _ in hashes)


def decode_access_token(token: str) -> TokenPayload:
    if not isinstance(token, str):
        raise TypeError(f"token must be of type str, not {type(token).__name__}.")
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        exp = payload.get("exp")

        if not sub:
            raise InvalidTokenError("Missing subject in decoded token.")

        if exp is None:
            raise InvalidTokenError("Missing expiration in decoded token.")

        if not isinstance(exp, (int, float)):
            raise TypeError(
                f"""
                Expiration in decoded token is not an int or float, 
                but an invalid type of: {type(exp).__name__}."""
            )

        expires_at = datetime.fromtimestamp(exp, tz=timezone.utc)
        token_payload = TokenPayload(employee_id=sub, expires_at=expires_at)
        return token_payload

    except ExpiredSignatureError as e:
        logger.error(
            msg=f"Could not validate credentials: Token has expired. {e}",
            exc_info=True,
            stack_info=True
        )
        raise e

    except InvalidTokenError as e:
        logger.error(
            msg=f"Could not validate credentials: Invalid token. {e}",
            exc_info=True,
            stack_info=True
        )
        raise e

def get_employee_token(token: str) -> TokenPayload:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    internal_server_error = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error.",
    )
    try:
        token_payload = decode_access_token(token)
        return token_payload
    except ExpiredSignatureError:
        credentials_exception.detail += ": Token has expired."
        raise credentials_exception
    except InvalidTokenError:
        credentials_exception.detail += ": Invalid token."
        raise credentials_exception
    except Exception as e:
        logger.error(
            msg=f"Caught Exception in function get_current_employee_token in src.core.security.py: {e}",
            exc_info=True,
            stack_info=True
        )
        raise internal_server_error


async def get_current_employee_token(token: str = Depends(oauth2)):
    return get_employee_token(token)