import pytest
import os
import sys
from fastapi.testclient import TestClient

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.db.database import get_db, SessionLocal, create_tables
from scripts.seed_data import seed_database

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    create_tables()
    seed_database()
    yield

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
