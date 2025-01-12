from datetime import date

from pydantic import BaseModel


class MassReadingPut(BaseModel):
    mass: float


class MassReading(MassReadingPut):
    date: date
