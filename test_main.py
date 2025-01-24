from fastapi.testclient import TestClient
from main import app
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from database import Base

# Create a separate test database (or use SQLite in-memory for fast testing)
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables in test database
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

test_client = TestClient(app)

import pytest
from database import Base

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_db():
    """Drop and recreate tables before each test."""
    Base.metadata.drop_all(bind=engine)  # Drop tables
    Base.metadata.create_all(bind=engine)  # Recreate tables



def test_add_ingredient():
    response = test_client.post("/items/", json={"name": "bun", "quantity": 10})
    assert response.status_code == 200
    assert response.json()["name"] == "bun"
    assert response.json()["quantity"] == 10

def test_get_available_burgers():
    test_client.post("/items/", json={"name": "bun", "quantity": 11})
    test_client.post("/items/", json={"name": "beef patty", "quantity": 20})
    test_client.post("/items/", json={"name": "lettuce", "quantity": 15})
    test_client.post("/items/", json={"name": "tomato", "quantity": 11})
    test_client.post("/items/", json={"name": "ketchup", "quantity": 12})
    response = test_client.get("/burgers/available/")
    assert response.status_code == 200
    assert response.json()["burgers_available"] == 11