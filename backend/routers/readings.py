from typing import List
from datetime import date

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from schemas.mass_reading import MassReading, MassAndDateReading, Reading
from models._database import get_db
from models.mass_reading import MassReading as MassReadingTable

router = APIRouter()


@router.get("/")
async def list_readings(db: Session = Depends(get_db)) -> List[Reading]:
    return db.query(MassReadingTable).order_by(MassReadingTable.id)


@router.post("/", status_code=201)
async def post_reading(
    mass_reading_post: MassAndDateReading, db: Session = Depends(get_db)
) -> Reading:
    existing_mass_reading = (
        db.query(MassReadingTable)
        .filter(MassReadingTable.date == mass_reading_post.date)
        .first()
    )
    if existing_mass_reading:
        existing_mass_reading.mass = mass_reading_post.mass
        db.commit()
        db.refresh(existing_mass_reading)

        return existing_mass_reading

    new_mass_reading = MassReadingTable(**mass_reading_post.model_dump())
    db.add(new_mass_reading)
    db.commit()

    return new_mass_reading


@router.delete("/{date}/")
async def delete_reading(date: date, db: Session = Depends(get_db)) -> Reading:
    mass_reading = db.query(MassReadingTable).filter(MassReadingTable.date == date).first()
    if not mass_reading:
        raise HTTPException(status_code=404, detail="Mass not found")

    db.delete(mass_reading)
    db.commit()

    return mass_reading


@router.put("/{date}/")
async def put_reading(date: date, mass_reading_put: MassReading, db: Session = Depends(get_db)) -> Reading:
    mass_reading = db.query(MassReadingTable).filter(MassReadingTable.date == date).first()
    if not mass_reading:
        raise HTTPException(status_code=404, detail="Mass reading not found")
    
    for key, value in mass_reading_put.model_dump(exclude_unset=True).items():
        setattr(mass_reading, key, value)

    db.commit()
    db.refresh(mass_reading)

    return mass_reading