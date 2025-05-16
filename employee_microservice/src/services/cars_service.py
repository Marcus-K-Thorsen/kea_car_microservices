# External Library imports
from typing import List, Optional

# Internal library imports
from src.database_management import Session
from src.repositories import (
    CustomerRepository,
    CarRepository,
    EmployeeRepository,
    ColorRepository,
    InsuranceRepository,
    AccessoryRepository,
    PurchaseRepository,
    ModelRepository
)
from src.resources import (
    CarReturnResource,
    CarCreateResource,
    RoleEnum
)
from src.exceptions import (
    UnableToFindIdError,
    UnableToDeleteAnotherEmployeesCarError,
    TheColorIsNotAvailableInModelToGiveToCarError,
    UnableToDeleteCarWithoutDeletingPurchaseTooError
)
from src.entities import (
    CustomerEntity,
    EmployeeEntity,
    AccessoryEntity,
    InsuranceEntity
)
from src.core import (
    TokenPayload, 
    get_current_employee
)


def get_all(
        session: Session,
        token: TokenPayload,
        customer_id: Optional[str] = None,
        employee_id: Optional[str] = None,
        is_purchased: Optional[bool] = None,
        is_past_purchase_deadline: Optional[bool] = None,
        car_limit: Optional[int] = None
) -> List[CarReturnResource]:

    car_repository = CarRepository(session)
    customer_repository = CustomerRepository(session)
    employee_repository = EmployeeRepository(session)
    purchase_repository = PurchaseRepository(session)

    if not (isinstance(customer_id, str) or customer_id is None):
        raise TypeError(f"customer_id must be of type str or None, "
                        f"not {type(customer_id).__name__}.")
    if not (isinstance(employee_id, str) or employee_id is None):
        raise TypeError(f"employee_id must be of type str or None, "
                        f"not {type(employee_id).__name__}.")

    if not (isinstance(is_purchased, bool) or is_purchased is None):
        raise TypeError(f"is_purchased must be of type bool or None, "
                        f"not {type(is_purchased).__name__}.")
    if not (isinstance(is_past_purchase_deadline, bool) or is_past_purchase_deadline is None):
        raise TypeError(f"is_past_purchase_deadline must be of type bool or None, "
                        f"not {type(is_past_purchase_deadline).__name__}.")
    if isinstance(car_limit, bool) or not (isinstance(car_limit, int) or car_limit is None):
        raise TypeError(f"car_limit must be of type int or None, "
                        f"not {type(car_limit).__name__}.")
        
    current_employee = get_current_employee(
        token,
        session,
        current_user_action="get_all cars"
    )
    
    if current_employee.role == RoleEnum.sales_person:
        employee_id = current_employee.id

    filtered_customer: Optional[CustomerEntity] = None
    if customer_id is not None:
        filtered_customer = customer_repository.get_by_id(customer_id)
        if filtered_customer is None:
            raise UnableToFindIdError(
                entity_name="Customer",
                entity_id=customer_id
            )
    
    filtered_employee = Optional[EmployeeEntity] = None
    if employee_id is not None:
        filtered_employee = employee_repository.get_by_id(employee_id)
        if filtered_employee is None:
            raise UnableToFindIdError(
                entity_name="Employee",
                entity_id=employee_id
            )

    cars = car_repository.get_all(
        customer=filtered_customer,
        employee=filtered_employee,
        is_purchased=is_purchased,
        is_past_purchase_deadline=is_past_purchase_deadline,
        limit=car_limit
    )
    
    car_resources = List[CarReturnResource] = []
    for car in cars:
        is_car_purchased: bool = purchase_repository.is_car_taken(car)
        car_resources.append(car.as_resource(is_car_purchased))
    
    return car_resources


def get_by_id(
        session: Session,
        token: TokenPayload, 
        car_id: str
) -> Optional[CarReturnResource]:

    car_repository = CarRepository(session)
    purchase_repository = PurchaseRepository(session)
    
    if not isinstance(car_id, str):
        raise TypeError(f"car_id must be of type str, "
                        f"not {type(car_id).__name__}.")
        
    get_current_employee(
        token,
        session,
        current_user_action="get car by id",
        valid_roles=[
            RoleEnum.manager,
            RoleEnum.admin
        ]
    )

    car = car_repository.get_by_id(car_id)
    
    if car is None:
        raise UnableToFindIdError(
            entity_name="Car",
            entity_id=car_id
        )
        
    is_car_purchased: bool = purchase_repository.is_car_taken(car)
    
    return car.as_resource(is_car_purchased)


def create(
        session: Session,
        token: TokenPayload,
        car_create_data: CarCreateResource
) -> CarReturnResource:
    
    car_repository = CarRepository(session)
    customer_repository = CustomerRepository(session)
    employee_repository = EmployeeRepository(session)
    model_repository = ModelRepository(session)
    color_repository = ColorRepository(session)
    accessory_repository = AccessoryRepository(session)
    insurance_repository = InsuranceRepository(session)
    
    if not isinstance(car_create_data, CarCreateResource):
        raise TypeError(f"car_create_data must be of type CarCreateResource, "
                        f"not {type(car_create_data).__name__}.")
        
    current_employee = get_current_employee(
        token,
        session,
        current_user_action="create car"
    )
    
    car_customer_id = str(car_create_data.customers_id)
    car_employee_id = car_create_data.employees_id
    if current_employee.role == RoleEnum.sales_person or car_employee_id is None:
        car_employee_id = current_employee.id
    else:
        car_employee_id = str(car_employee_id)
    car_model_id = str(car_create_data.models_id)
    car_color_id = str(car_create_data.colors_id)
    car_accessory_ids = [str(accessory_id) for accessory_id in car_create_data.accessory_ids]
    car_insurance_ids = [str(insurance_id) for insurance_id in car_create_data.insurance_ids]
    
    customer_for_the_car = customer_repository.get_by_id(car_customer_id)
    if customer_for_the_car is None:
        raise UnableToFindIdError("Customer", car_customer_id)

    employee_for_the_car = employee_repository.get_by_id(car_employee_id)
    if employee_for_the_car is None:
        raise UnableToFindIdError("Employee", car_employee_id)

    model_for_the_car = model_repository.get_by_id(car_model_id)
    if model_for_the_car is None:
        raise UnableToFindIdError("Model", car_model_id)

    color_for_the_car = color_repository.get_by_id(car_color_id)
    if color_for_the_car is None:
        raise UnableToFindIdError("Color", car_color_id)

    if car_color_id not in [color.id for color in model_for_the_car.colors]:
        raise TheColorIsNotAvailableInModelToGiveToCarError(model_for_the_car, color_for_the_car)

    accessories_for_the_car: List[AccessoryEntity] = []
    for accessory_id in car_accessory_ids:
        accessory_for_the_car = accessory_repository.get_by_id(accessory_id)
        if accessory_for_the_car is None:
            raise UnableToFindIdError(
                entity_name="Accessory",
                entity_id=accessory_id
            )
        accessories_for_the_car.append(accessory_for_the_car)

    insurances_for_the_car: List[InsuranceEntity] = []
    for insurance_id in car_insurance_ids:
        insurance_for_the_car = insurance_repository.get_by_id(insurance_id)
        if insurance_for_the_car is None:
            raise UnableToFindIdError(
                entity_name="Insurance",
                entity_id=insurance_id
            )
        insurances_for_the_car.append(insurance_for_the_car)

    newly_created_car = car_repository.create(
        car_create_data,
        customer_for_the_car,
        employee_for_the_car,
        model_for_the_car,
        color_for_the_car,
        accessories_for_the_car,
        insurances_for_the_car
    )
    
    return newly_created_car.as_resource(is_purchased=False)


def delete(
        session: Session,
        token: TokenPayload,
        car_id: str, 
        delete_purchase_too: bool
) -> None:

    car_repository = CarRepository(session)
    purchase_repository = PurchaseRepository(session)
    
    if not isinstance(car_id, str):
        raise TypeError(f"car_id must be of type str, "
                        f"not {type(car_id).__name__}.")
    if not isinstance(delete_purchase_too, bool):
        raise TypeError(f"delete_purchase_too must be of type bool, "
                        f"not {type(delete_purchase_too).__name__}.")
        
    current_employee = get_current_employee(
        token,
        session,
        current_user_action="delete car"
    )

    car_to_delete = car_repository.get_by_id(car_id)
    if car_to_delete is None:
        raise UnableToFindIdError(
            entity_name="Car",
            entity_id=car_id
        )
        
    current_employee_id = current_employee.id
    employee_id_of_car_to_delete = car_to_delete.employee.id
    
    if current_employee.role == RoleEnum.sales_person and current_employee_id != employee_id_of_car_to_delete:
        raise UnableToDeleteAnotherEmployeesCarError(
            current_employee,
            car_to_delete
        )
        
    car_has_been_purchased = purchase_repository.is_car_taken(car_to_delete)
    if not delete_purchase_too and car_has_been_purchased:
        raise UnableToDeleteCarWithoutDeletingPurchaseTooError(car_to_delete)

    car_repository.delete(car_to_delete, delete_purchase_too)
