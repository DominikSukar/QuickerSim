from typing import List
from datetime import date

from fastapi import APIRouter

from schemas.mass_reading import MassReading

router = APIRouter()


@router.get("/")
async def list_readings() -> List[MassReading]:
    return None


@router.post("/")
async def post_reading() -> MassReading:
    return None


@router.delete("/{date}")
async def delete_reading(date: date) -> MassReading:
    return None


@router.put("/{date}")
async def put_reading(date: date) -> MassReading:
    return None
