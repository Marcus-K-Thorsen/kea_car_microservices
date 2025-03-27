# External Library imports
from typing import List, Optional
from pymongo.database import Database

# Internal library imports
from src.exceptions import UnableToFindIdError
from src.repositories import InsuranceRepository
from src.resources import InsuranceReturnResource


def get_all(
        database: Database,
        insurances_limit: Optional[int] = None
) -> List[InsuranceReturnResource]:
    
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
