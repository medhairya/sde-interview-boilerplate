import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.db import Base, get_db
from src.app import app

# Sandboxed database for tests - runs entirely in-memory and isolates tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """
    Creates a fresh, isolated database schema and session for each test run.
    Recreates and teardowns tables between each test for complete state isolation.
    """
    # Create the schema in the test database
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop everything to avoid state pollution between runs
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """
    Provides a FastAPI TestClient configured to override the database session
    dependency with the isolated test session.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    # Override app's database connection injection
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client

    # Clean up overrides after test completes to prevent side effects
    app.dependency_overrides.clear()
