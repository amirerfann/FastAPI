from pydantic import BaseModel, field_validator, Field, field_serializer

from typing import Optional

class PersonBaseSchemas(BaseModel):
    name: Optional[str] = None

    @field_validator("name")
    def name_validator(cls, value):
        if value is None:
            return value
        if len(value) > 25:
            raise ValueError("name must be less than 25 characters")
        if not value.isalpha():
            raise ValueError("you can use only letters")
        return value

    @field_serializer("name")
    def serializer_name(self, value):
        return value.title() if value else value

class PersonCreateSchemas(PersonBaseSchemas):
    pass 

class ResponseSchemas(PersonBaseSchemas):
    id: int

class PersonResponseSchemas(PersonBaseSchemas):
    pass

class UpdateSchemas(PersonBaseSchemas):
    id: int 
