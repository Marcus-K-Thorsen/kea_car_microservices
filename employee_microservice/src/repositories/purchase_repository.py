# External Library imports
from typing import Optional, List

# Internal library imports
from src.resources import PurchaseCreateResource
from src.repositories.base_repository import BaseRepository
from src.entities import (
    CarEntity,
    PurchaseEntity,
    EmployeeEntity
)



class PurchaseRepository(BaseRepository):

    def get_all(self, employee: Optional[EmployeeEntity], limit: Optional[int] = None) -> List[PurchaseEntity]:
        """
        Retrieves a list of purchases from the Employee MySQL database.
        
        :param employee: Filter for purchases by employee (optional).
        :type employee: EmployeeEntity | None
        :param limit: The maximum number of purchases to retrieve (optional).
        :type limit: int | None
        :return: A list of purchases.
        :rtype: List[PurchaseEntity]
        """
        purchases_query = self.session.query(PurchaseEntity)
        if self.limit_is_valid(limit):
            purchases_query = purchases_query.limit(limit)
        if employee is not None and isinstance(employee, EmployeeEntity):
            return [purchase for purchase in purchases_query.all() if purchase.cars_id == employee.id]
        return purchases_query.all()


    def get_by_id(self, purchase_id: str) -> Optional[PurchaseEntity]:
        """
        Retrieves a purchase by ID from the Employee MySQL database.
        
        :param purchase_id: The ID of the purchase to retrieve.
        :type purchase_id: str
        :return: The purchase if found, None otherwise.
        :rtype: PurchaseEntity | None
        """
        return self.session.get(PurchaseEntity, purchase_id)

    def get_by_car_id(self, car: CarEntity) -> Optional[PurchaseEntity]:
        """
        Retrieves a purchase by car ID from the Employee MySQL database.
        
        :param car: The car entity to retrieve the purchase for.
        :type car: CarEntity
        :return: The purchase if there is a car attached to that purchase found, None otherwise.
        :rtype: PurchaseEntity | None
        """
        return self.session.query(PurchaseEntity).filter_by(cars_id=car.id).first()
    

    def create(
        self, 
        purchase_create_data: PurchaseCreateResource,
        car_to_purchase: CarEntity
    ) -> PurchaseEntity:
        """
        Creates a new purchase in the Employee MySQL database.
        
        :param purchase_create_data: The data for the purchase to create.
        :type purchase_create_data: PurchaseCreateResource
        :param car_to_purchase: The car entity that is being purchased
        :type car_to_purchase: CarEntity
        :return: The created purchase entity.
        :rtype: PurchaseEntity
        """
        new_purchase = PurchaseEntity(
            id=str(purchase_create_data.id),
            cars_id=car_to_purchase.id,
            date_of_purchase=purchase_create_data.date_of_purchase
        )
        self.session.add(new_purchase)
        self.session.flush()
        self.session.refresh(new_purchase)

        return new_purchase


    def is_car_taken(self, car: CarEntity) -> bool:
        """
        Checks if a car is already purchased.
        
        :param car: The car entity to check.
        :type car: CarEntity
        :return: True if the car is purchased, False otherwise.
        :rtype: bool
        """
        return self.session.query(PurchaseEntity).filter_by(cars_id=car.id).first() is not None
