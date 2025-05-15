# Internal library imports
from src.entities.base_entity import BaseEntity


class InsuranceBaseEntity(BaseEntity):
    name: str
    price: float
    
class InsuranceEntity(InsuranceBaseEntity):
    pass

class InsuranceMessage(InsuranceBaseEntity):
    pass
