# External Library imports
from typing import List, Optional


# Internal library imports
from src.database_management import Session
from src.entities import EmployeeEntity
from src.repositories import (
    CarRepository,
    PurchaseRepository,
    EmployeeRepository
)
from src.resources import (
    PurchaseReturnResource,
    PurchaseCreateResource,
    RoleEnum
)
from src.exceptions import (
    EmployeeIsNotAllowedToRetrieveOrMakeCarPurchasesBasedOnOtherEmployeeError,
    PurchaseDeadlineHasPastError,
    AlreadyTakenFieldValueError,
    UnableToFindEntityError,
    UnableToFindIdError
)
from src.core import (
    TokenPayload, 
    get_current_employee
)

def get_all(
        session: Session,
        token: TokenPayload,
        employee_id: Optional[str] = None,
        purchase_limit: Optional[int] = None
)  -> List[PurchaseReturnResource]:

    purchase_repository = PurchaseRepository(session)
    employee_repository = EmployeeRepository(session)
    
    if isinstance(purchase_limit, bool) or not (isinstance(purchase_limit, int) or purchase_limit is None):
        raise TypeError(f"purchase_limit must be of type int or None, "
                        f"not {type(purchase_limit).__name__}.")
    if not (isinstance(employee_id, str) or employee_id is None):
        raise TypeError(f"employee_id must be of type str or None, "
                        f"not {type(employee_id).__name__}.")
        
    current_employee = get_current_employee(token, session, current_user_action="get_all purchases")
    
    if current_employee.role == RoleEnum.sales_person:
        employee_id = current_employee.id
        
    filtered_employee: Optional[EmployeeEntity] = None
    if employee_id is not None:
        filtered_employee = employee_repository.get_by_id(employee_id)
        if filtered_employee is None:
            raise UnableToFindIdError(
                entity_name="Employee",
                entity_id=employee_id
            )
    
    purchases = purchase_repository.get_all(employee=filtered_employee, limit=purchase_limit)
    
    return [purchase.as_resource() for purchase in purchases]

def get_by_id(
        session: Session,
        token: TokenPayload,
        purchase_id: str
) -> PurchaseReturnResource:

    repository = PurchaseRepository(session)
    
    if not isinstance(purchase_id, str):
        raise TypeError(f"purchase_id must be of type str, "
                        f"not {type(purchase_id).__name__}.")
        
    current_employee = get_current_employee(
        token,
        session,
        current_user_action="get purchase by id"
    )

    purchase = repository.get_by_id(purchase_id)
    if purchase is None:
        raise UnableToFindIdError(
            entity_name="Purchase",
            entity_id=purchase_id
        )
    
    if current_employee.role == RoleEnum.sales_person and purchase.car.employees_id != current_employee.id:
        raise EmployeeIsNotAllowedToRetrieveOrMakeCarPurchasesBasedOnOtherEmployeeError(
            current_employee=current_employee
        )

    return purchase.as_resource()


def get_by_car_id(
        session: Session,
        token: TokenPayload,
        car_id: str
) -> PurchaseReturnResource:

    car_repository = CarRepository(session)
    purchase_repository = PurchaseRepository(session)
    
    if not isinstance(car_id, str):
        raise TypeError(f"car_id must be of type str, "
                        f"not {type(car_id).__name__}.")
        
    current_employee = get_current_employee(
        token,
        session,
        current_user_action="get purchase by car id"
    )

    car = car_repository.get_by_id(car_id)
    if car is None:
        raise UnableToFindIdError(
            entity_name="Car",
            entity_id=car_id
        )
        
    if current_employee.role == RoleEnum.sales_person and current_employee.id != car.employees_id:
        raise EmployeeIsNotAllowedToRetrieveOrMakeCarPurchasesBasedOnOtherEmployeeError(
            current_employee=current_employee
        )

    purchase = purchase_repository.get_by_car_id(car)
    if purchase is None:
        raise UnableToFindEntityError(
            entity_name="Purchase",
            field="cars_id",
            value=car_id
        )

    return purchase.as_resource()

def create(
        session: Session,
        token: TokenPayload,
        purchase_create_data: PurchaseCreateResource
) -> PurchaseReturnResource:

    car_repository = CarRepository(session)
    purchase_repository = PurchaseRepository(session)
    
    if not isinstance(purchase_create_data, PurchaseCreateResource):
        raise TypeError(f"purchase_create_data must be of type PurchaseCreateResource, "
                        f"not {type(purchase_create_data).__name__}.")

    car_id: str = str(purchase_create_data.cars_id)
    car = car_repository.get_by_id(car_id)
    if car is None:
        raise UnableToFindIdError(
            entity_name="Car",
            entity_id=car_id
        )
        
    current_employee = get_current_employee(
        token,
        session,
        current_user_action="create purchase"
    )
    
    if current_employee.role == RoleEnum.sales_person and car.employees_id != current_employee.id:
        raise EmployeeIsNotAllowedToRetrieveOrMakeCarPurchasesBasedOnOtherEmployeeError(
            current_employee=current_employee
        )
        
    aleady_created_purchase = purchase_repository.get_by_id(str(purchase_create_data.id))
    if aleady_created_purchase is not None:
        return aleady_created_purchase.as_resource()

    if purchase_repository.is_car_taken(car):
        raise AlreadyTakenFieldValueError(
            entity_name="Purchase",
            field="cars_id",
            value=car_id
        )

    date_of_purchase = purchase_create_data.date_of_purchase
    if car.purchase_deadline < date_of_purchase:
        raise PurchaseDeadlineHasPastError(car, date_of_purchase)

    created_purchased = purchase_repository.create(
        purchase_create_data,
        car_to_purchase=car
        )
    
    return created_purchased.as_resource()

