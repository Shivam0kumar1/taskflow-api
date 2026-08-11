import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_test_db, get_db
from config import TEST_DATABASE_URL
from init_postgres import init_postgresql
import psycopg2

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    init_postgresql(TEST_DATABASE_URL)
    yield

@pytest.fixture(autouse=True)
def clean_database():
    conn = psycopg2.connect(TEST_DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM jobs")
    cursor.execute("DELETE FROM users")

    conn.commit()
    conn.close()

@pytest.fixture()
def client():
    app.dependency_overrides[get_db] = get_test_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

@pytest.fixture()
def auth_headers(client):
    signup_response = client.post(
        "/signup",
        json={
            "username": "testuser",
            "password": "password123"
        }
    )
    assert signup_response.status_code == 200

    login_response = client.post(
        "/login",
        json={
            "username": "testuser",
            "password": "password123"
        }
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }