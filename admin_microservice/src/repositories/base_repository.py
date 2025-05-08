# External Library imports
from typing import Optional

# Internal library imports
from src.database_management import Session


class BaseRepository:
    def __init__(self, session: Session):
        if not isinstance(session, Session):
            raise TypeError(f"session must be of type Session, "
                            f"not {type(session).__name__}.")
        self.session = session

    def limit_is_valid(self, limit: Optional[int]) -> bool:
        """
        Validates whether a given limit is a positive integer.

        :param limit: The limit value to validate.
        :type limit: int | None
        :return: True if the limit is valid, False otherwise.
        :rtype: bool
        """
        return limit is not None and isinstance(limit, int) and limit > 0
