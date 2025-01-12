from datetime import date

from pydantic import BaseModel

class MassReading(BaseModel):
    date: date
    mass: float