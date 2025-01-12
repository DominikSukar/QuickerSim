from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from utils.env import DATABASE_LOGIN, DATABASE_PASSWORD

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DATABASE_LOGIN}:{DATABASE_PASSWORD}@localhost:5432"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()