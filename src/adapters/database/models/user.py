from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    name = Column(String, nullable=False)

    schedule = relationship("Schedule", back_populates="user")
