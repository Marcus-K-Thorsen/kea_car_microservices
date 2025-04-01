"""
**Base Repository Module**

This module defines the `BaseRepository` class, which serves as the foundation for all
repository classes in the system. It provides common functionality for interacting with
MongoDB collections and validating query parameters.

Key Responsibilities:

- Provide access to MongoDB collections for various entities.
- Validate query parameters such as limits.
"""

# External Library imports
from typing import Optional
from pymongo.collection import Collection

# Internal library imports
from src.database_management import Database


class BaseRepository:
    """
    Base class for all repository classes.

    This class provides shared functionality for interacting with the database, such as
    retrieving MongoDB collections and validating query parameters. All other repository
    classes inherit from this base class.

    Attributes:
        database (Database): The database instance used for interacting with MongoDB.
    """

    def __init__(self, database: Database):
        """
        Initializes the `BaseRepository` with a database instance.

        :param database: The database instance used for interacting with MongoDB.
        :type database: Database
        :raises TypeError: If the provided database is not of type `Database`.
        """
        if not isinstance(database, Database):
            raise TypeError(f"database must be of type Database, "
                            f"not {type(database).__name__}.")
        self.database = database

    def limit_is_valid(self, limit: Optional[int]) -> bool:
        """
        Validates whether a given limit is a positive integer.

        :param limit: The limit value to validate.
        :type limit: int | None
        :return: True if the limit is valid, False otherwise.
        :rtype: bool
        """
        return limit is not None and isinstance(limit, int) and limit > 0

    def get_models_collection(self) -> Collection:
        """
        Retrieves the MongoDB collection for car models.

        :return: The MongoDB collection for car models.
        :rtype: Collection
        """
        return self.database.get_collection("models")

    def get_brands_collection(self) -> Collection:
        """
        Retrieves the MongoDB collection for car brands.

        :return: The MongoDB collection for car brands.
        :rtype: Collection
        """
        return self.database.get_collection("brands")

    def get_colors_collection(self) -> Collection:
        """
        Retrieves the MongoDB collection for colors.

        :return: The MongoDB collection for colors.
        :rtype: Collection
        """
        return self.database.get_collection("colors")

    def get_accessories_collection(self) -> Collection:
        """
        Retrieves the MongoDB collection for accessories.

        :return: The MongoDB collection for accessories.
        :rtype: Collection
        """
        return self.database.get_collection("accessories")

    def get_insurances_collection(self) -> Collection:
        """
        Retrieves the MongoDB collection for insurances.

        :return: The MongoDB collection for insurances.
        :rtype: Collection
        """
        return self.database.get_collection("insurances")
