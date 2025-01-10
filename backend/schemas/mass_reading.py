import datetime

from pydantic import BaseModel

class MassReading(BaseModel):
    date: datetime.datetime
    mass: float