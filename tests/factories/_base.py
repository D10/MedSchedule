from typing import Type

import factory

from src.adapters.database.models.base import Base as BaseModel


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory): ...
