import pytest
from typing import Generator, Dict
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.config import settings
from app.models.database import Base, get_db

# Create test database engine
TEST_SQLALCHEMY_DATABASE_URL = "postgresql://test_user:test_password@localhost/test_db"
engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)

# Create test database session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db() -> Generator:
    """
    Database fixture for tests
    Creates tables before tests and drops them after
    """
    Base.metadata.create_all(bind=engine)
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client() -> Generator:
    """
    TestClient fixture for making API requests
    """
    with TestClient(app) as c:
        yield c

@pytest.fixture
def api_key_headers() -> Dict[str, str]:
    """
    Headers with API key for authenticated requests
    """
    return {settings.API_KEY_NAME: settings.API_KEY}