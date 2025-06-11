# External Library imports
from typing import Optional, List

# Internal library imports
from src.resources import ModelCreateResource
from src.repositories.base_repository import BaseRepository
from src.entities import ModelEntity, BrandEntity, ColorEntity, models_has_colors

class ModelRepository(BaseRepository):
    def get_all(
            self,
            brand: Optional[BrandEntity] = None,
            limit: Optional[int] = None
    ) -> List[ModelEntity]:
        """
        Retrieves all models from the Employee MySQL database.
        
        :param brand: The brand to filter models by (optional).
        :type brand: BrandEntity | None
        :param limit: The maximum number of models to retrieve (optional).
        :type limit: int | None
        :return: A list of ModelEntity objects.
        :rtype: list[ModelEntity]
        """
        models_query = self.session.query(ModelEntity)
        if brand is not None and isinstance(brand, BrandEntity):
            models_query = models_query.filter_by(brands_id=brand.id)

        if self.limit_is_valid(limit):
            models_query = models_query.limit(limit)

        return models_query.all()


    def get_by_id(self, model_id: str) -> Optional[ModelEntity]:
        """
        Retrieves a model by ID from the Employee MySQL database.
        
        :param model_id: The ID of the model to retrieve.
        :type model_id: str
        :return: A ModelEntity object if found, None otherwise.
        :rtype: ModelEntity | None
        """
        return self.session.get(ModelEntity, model_id)
    
    
    def create(
            self,
            model_create_data: ModelCreateResource,
            model_image_url: str,
            brand_entity: BrandEntity,
            color_entities: List[ColorEntity]
    ) -> ModelEntity:
        """
        Creates a new model in the Employee MySQL database.
        
        :param model_create_data: The data for the model to create.
        :type model_create_data: ModelCreateResource
        :param model_image_url: The URL of the model's image.
        :type model_image_url: str
        :param brand_entity: The brand entity associated with the model.
        :type brand_entity: BrandEntity
        :param color_entities: A list of color entities associated with the model.
        :type color_entities: List[ColorEntity]
        :return: The created ModelEntity object.
        :rtype: ModelEntity
        """
        model_id = str(model_create_data.id)
        new_model = ModelEntity(
            id=model_id,
            name=model_create_data.name,
            price=model_create_data.price,
            image_url=model_image_url,
            brands_id=brand_entity.id
        )
        self.session.add(new_model)
        self.session.flush()
        
        for color in color_entities:
            insert = models_has_colors.insert(
            ).values(models_id=model_id, colors_id=color.id)
            self.session.execute(insert)
        
        self.session.flush()
        self.session.refresh(new_model)
        
        return new_model
    