from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_read_users():
    response = client.get("/v1/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_role_not_found():
    response = client.get("/v1/roles/999")  # ID inexistente
    assert response.status_code == 404
    assert response.json()["detail"] == "Role not found"

def test_create_user_role_not_found():
    user_data = {
        "name": "testuser",
        "email": "testuser@example.com",
        "role_id": 999,
        "password": ""
    }
    response = client.post("/v1/users/", json=user_data)
    assert response.status_code == 400
    assert response.json()["error"] == "Role not found. Please create a role first."

def test_create_role():
    role_data = {
        "description": "Test Role"
    }
    response = client.post("/v1/roles/", json=role_data)
    assert response.status_code == 200
    assert response.json()["description"] == "Test Role"
