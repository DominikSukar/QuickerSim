import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database

from models._database import Base, get_db
from main import app
from utils.env import DATABASE_LOGIN, DATABASE_PASSWORD


@pytest.fixture(scope="class")
def mock_client():
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{DATABASE_LOGIN}:{DATABASE_PASSWORD}@localhost:5432/quickersim_test_database"
    )

    if not database_exists(SQLALCHEMY_DATABASE_URL):
        create_database(SQLALCHEMY_DATABASE_URL)
    
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    yield client

    Base.metadata.drop_all(bind=engine)
    drop_database(SQLALCHEMY_DATABASE_URL)
