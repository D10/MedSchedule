from pydantic import BaseModel


class Entity(BaseModel):
    class Config:
        validate_assignment = True
