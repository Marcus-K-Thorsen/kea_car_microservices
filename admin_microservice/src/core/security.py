# External Library imports
import hashlib
import requests

# Internal Library imports
from src.exceptions import log_and_raise_error
from src.core.config import pwd_context

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

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