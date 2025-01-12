from datetime import date

from pydantic import BaseModel, field_validator


class MassReadingPut(BaseModel):
    mass: float


class MassReading(MassReadingPut):
    date: date

    @field_validator("date")
    def validate_date(cls, value):
        if value and value > date.today():
            raise ValueError("The date cannot be in the future.")
        return value
