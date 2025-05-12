# External Library imports
from jwt import encode

# Internal library imports
from src.core.tokens import (
    EmployeeReturnResource,
    TokenData,
    Token
)
from src.core.config import (
    pwd_context,
    SECRET_KEY,
    ALGORITHM
)


def verify_password(
        sent_login_password: str,
        found_hashed_password: str
) -> bool:
    return pwd_context.verify(sent_login_password, found_hashed_password)


def create_access_token(employee: EmployeeReturnResource) -> Token:
    data: TokenData = TokenData(sub=employee.id)
    encoded_jwt = encode(data.model_dump(), SECRET_KEY, algorithm=ALGORITHM)
    return Token(access_token=encoded_jwt, token_type="bearer", employee=employee)

