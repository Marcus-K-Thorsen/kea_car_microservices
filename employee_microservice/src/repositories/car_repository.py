# External Library imports
from datetime import date
from typing import Optional, List
from sqlalchemy import exists


# Internal library imports
from src.logger_tool import logger
from src.resources import CarCreateResource
from src.repositories.base_repository import BaseRepository
from src.entities import (
    CarEntity,
    ColorEntity,
    ModelEntity,
    PurchaseEntity, 
    CustomerEntity,
    EmployeeEntity,
    AccessoryEntity,
    InsuranceEntity,
    cars_has_accessories, 
    cars_has_insurances
)



def calculate_total_price_for_car(
        model_entity: ModelEntity,
        color_entity: ColorEntity,
        accessory_entities: List[AccessoryEntity],
        insurance_entities: List[InsuranceEntity]
) -> float:
    total_price: float = 0.0
    total_price += model_entity.price + color_entity.price
    for accessory in accessory_entities:
        total_price += accessory.price
    for insurance in insurance_entities:
        total_price += insurance.price

    # Round total_price to 2 decimal places before returning
    total_price = round(total_price, 2)
    return total_price



class CarRepository(BaseRepository):

    def get_all(
            self,
            customer: Optional[CustomerEntity] = None,
            employee: Optional[EmployeeEntity] = None,
            is_purchased: Optional[bool] = None,
            is_past_purchase_deadline: Optional[bool] = None,
            limit: Optional[int] = None
    ) -> List[CarEntity]:
        """
        Retrieves a list of cars from the Employee MySQL database based on various filters.
        
        :param customer: Filter for cars by customer (optional).
        :type customer: CustomerEntity | None
        :param employee: Filter for cars by employee (optional).
        :type employee: EmployeeEntity | None
        :param is_purchased: Filter for cars by purchase status (optional).
        :type is_purchased: bool | None
        :param is_past_purchase_deadline: Filter for cars by purchase deadline status (optional).
        :type is_past_purchase_deadline: bool | None
        :param limit: The maximum number of cars to retrieve (optional).
        :type limit: int | None
        :return: A list of cars.
        :rtype: List[CarEntity]
        """
        cars_query = self.session.query(CarEntity)
        if customer is not None and isinstance(customer, CustomerEntity):
            cars_query = cars_query.filter_by(customers_id=customer.id)
        if employee is not None and isinstance(employee, EmployeeEntity):
            cars_query = cars_query.filter_by(employees_id=employee.id)
        if is_purchased is not None and isinstance(is_purchased, bool):
            if is_purchased:
                cars_query = cars_query.filter(
                    exists().where(PurchaseEntity.cars_id == CarEntity.id)
                )
            else:
                cars_query = cars_query.filter(
                    ~exists().where(PurchaseEntity.cars_id == CarEntity.id)
                )
        if is_past_purchase_deadline is not None and isinstance(is_past_purchase_deadline, bool):
            current_date = date.today()
            if is_past_purchase_deadline:
                cars_query = cars_query.filter(CarEntity.purchase_deadline < current_date)
            else:
                cars_query = cars_query.filter(CarEntity.purchase_deadline >= current_date)

        if self.limit_is_valid(limit):
            cars_query = cars_query.limit(limit)

        return cars_query.all()


    def get_by_id(self, car_id: str) -> Optional[CarEntity]:
        """
        Retrieves a car by ID from the Employee MySQL database.
        
        :param car_id: The ID of the car to retrieve.
        :type car_id: str
        :return: The car if found, None otherwise.
        :rtype: CarEntity | None
        """
        return self.session.get(CarEntity, car_id)


    def create(
            self,
            car_create_data: CarCreateResource,
            customer: CustomerEntity,
            employee: EmployeeEntity,
            model: ModelEntity,
            color: ColorEntity,
            accessories: List[AccessoryEntity],
            insurances: List[InsuranceEntity]
    ) -> CarEntity:
        """
        Creates a new car in the Employee MySQL database.
        
        :param car_create_data: The data for the car to create.
        :type car_create_data: CarCreateResource
        :param customer: The customer associated with the car.
        :type customer: CustomerEntity
        :param employee: The employee associated with the car.
        :type employee: EmployeeEntity
        :param model: The model of the car.
        :type model: ModelEntity
        :param color: The color of the car.
        :type color: ColorEntity
        :param accessories: The accessories associated with the car.
        :type accessories: List[AccessoryEntity]
        :param insurances: The insurances associated with the car.
        :type insurances: List[InsuranceEntity]
        :return: The created car entity.
        :rtype: CarEntity
        """
        calculated_total_price_for_the_car = calculate_total_price_for_car(
            model,
            color,
            accessories,
            insurances
        )
        car_id = str(car_create_data.id)
        try:
            new_car = CarEntity(
                id=car_id,
                models_id=model.id,
                colors_id=color.id,
                customers_id=customer.id,
                employees_id=employee.id,
                total_price=calculated_total_price_for_the_car,
                purchase_deadline=car_create_data.purchase_deadline
            )

            self.session.add(new_car)
            self.session.flush()

            for accessory in accessories:
                insert = cars_has_accessories.insert(
                ).values(cars_id=car_id, accessories_id=accessory.id)
                self.session.execute(insert)

            for insurance in insurances:
                insert = cars_has_insurances.insert(
                ).values(cars_id=car_id, insurances_id=insurance.id)
                self.session.execute(insert)

            self.session.flush()
            self.session.refresh(new_car)
            return new_car
        except Exception as e:
            logger.error(f"There was an error while creating a car, so will be doing a rollback: {e}")
            self.session.rollback()
            raise


    def delete(self, car: CarEntity, delete_purchase_too: bool):
        """
        Deletes a car from the Employee MySQL database.
        
        :param car: The car to delete.
        :type car: CarEntity
        :param delete_purchase_too: Whether to delete the purchase associated with the car.
        :type delete_purchase_too: bool
        :return: None
        :rtype: None
        """
        car_id = car.id
        try:
            if delete_purchase_too:
                self.session.query(PurchaseEntity).filter_by(cars_id=car_id).delete()
                self.session.flush()
            self.session.query(CarEntity).filter_by(id=car_id).delete()
            self.session.flush()
        except Exception as e:
            logger.error(f"There was an error while deleting a car, so will be doing a rollback: {e}")
            self.session.rollback()
            raise 
