class IncorrectCredentialError(Exception):
    """Base class for exceptions related to incorrect credentials"""
    pass


class IncorrectEmailError(IncorrectCredentialError):
    """Exception raised for incorrect email"""

    def __init__(self, email: str):
        self.message = f"The email '{email}' is incorrect."
        super().__init__(self.message)  # Call the base class constructor

    def __str__(self):
        return f"{self.message}"


class IncorrectPasswordError(IncorrectCredentialError):
    """Exception raised for incorrect password"""

    def __init__(self, email: str, password: str):
        self.message = f"The password '{password}' is incorrect for the email '{email}'."
        super().__init__(self.message)  # Call the base class constructor

    def __str__(self):
        return f"{self.message}"
