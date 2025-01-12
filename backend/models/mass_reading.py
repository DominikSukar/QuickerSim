from sqlalchemy import Date, Float
from sqlalchemy.orm import Mapped, mapped_column

from models._database import Base


class MassReading(Base):
    """
    Table stores data about mass readings
    """

    __tablename__ = "mass_readings"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[int] = mapped_column(Date, nullable=False)
    float: Mapped[str] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return f"<MassReading {self.id}:{self.date}{self.float}>"
