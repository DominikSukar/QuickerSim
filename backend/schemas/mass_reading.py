from datetime import date

from pydantic import BaseModel, field_validator


class MassReadingPut(BaseModel):
    mass: float

    @field_validator("mass")
    def validate_mass(cls, value):
        if value and value < 0:
            raise ValueError("The mass must be greater than zero.")
        return value

class MassReading(MassReadingPut):
    id: int
    date: date

    @field_validator("date")
    def validate_date(cls, value):
        if value and value > date.today():
            raise ValueError("The date cannot be in the future.")
        return value
