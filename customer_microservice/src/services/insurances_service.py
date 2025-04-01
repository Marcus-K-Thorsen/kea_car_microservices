"""
**Insurances Service Module**

This module provides business logic for insurance-related operations.
It interacts with the `InsuranceRepository` to retrieve data from the database
and transforms it into resource representations for API responses.

Key Responsibilities:

- Retrieve all insurances with optional limits.
- Retrieve a specific insurance by its ID.
"""

# External Library imports
from typing import List, Optional

# Internal library imports
from src.database_management import Database
from src.exceptions import UnableToFindIdError
from src.repositories import InsuranceRepository
from src.resources import InsuranceReturnResource


def get_all(
        database: Database,
        insurances_limit: Optional[int] = None
) -> List[InsuranceReturnResource]:
    """
    Retrieves all insurances from the database, with an optional limit.

    This function interacts with the `InsuranceRepository` to fetch insurance data
    and converts it into a list of `InsuranceReturnResource` objects.

    :param database: The database connection instance.
    :type database: Database
    :param insurances_limit: The maximum number of insurances to retrieve (optional).
    :type insurances_limit: int | None
    :return: A list of insurances as `InsuranceReturnResource`.
    :rtype: List[InsuranceReturnResource]
    :raises TypeError: If `insurances_limit` is not of type `int` or `None`.
    """
    repository = InsuranceRepository(database)
    
    if isinstance(insurances_limit, bool) or not (isinstance(insurances_limit, int) or insurances_limit is None):
        raise TypeError(f"insurances_limit must be of type int or None, "
                        f"not {type(insurances_limit).__name__}.")

    insurances = repository.get_all(limit=insurances_limit)
    
    return [insurance.as_resource() for insurance in insurances]


def get_by_id(
        database: Database,
        insurance_id: str
) -> InsuranceReturnResource:
    """
    Retrieves a specific insurance by its ID.

    This function interacts with the `InsuranceRepository` to fetch a single insurance
    and converts it into an `InsuranceReturnResource` object.

    :param database: The database connection instance.
    :type database: Database
    :param insurance_id: The ID of the insurance to retrieve.
    :type insurance_id: str
    :return: The insurance as an `InsuranceReturnResource`.
    :rtype: InsuranceReturnResource
    :raises TypeError: If `insurance_id` is not of type `str`.
    :raises UnableToFindIdError: If no insurance is found with the given ID.
    """
    repository = InsuranceRepository(database)
    
    if not isinstance(insurance_id, str):
        raise TypeError(f"insurance_id must be of type str, "
                        f"not {type(insurance_id).__name__}.")

    insurance = repository.get_by_id(insurance_id)
    if insurance is None:
        raise UnableToFindIdError(
            entity_name="Insurance",
            entity_id=insurance_id
        )
        
    return insurance.as_resource()
