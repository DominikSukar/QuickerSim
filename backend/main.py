from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    readings
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"]
)

app.include_router(readings.router, tags=["Readings"], prefix="/readings")
