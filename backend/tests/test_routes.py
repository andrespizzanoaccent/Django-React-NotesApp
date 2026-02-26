import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import SessionLocal, Base, engine
from backend.models.category import Category

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_category():
    response = client.post("/categories", json={"name": "New Category"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Category"


def test_get_categories():
    client.post("/categories", json={"name": "Category 1"})
    client.post("/categories", json={"name": "Category 2"})

    response = client.get("/categories")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_update_category():
    response = client.post("/categories", json={"name": "Old Category"})
    category_id = response.json()["id"]

    update_response = client.put(f"/categories/{category_id}", json={"name": "Updated Category"})
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["name"] == "Updated Category"


def test_delete_category():
    response = client.post("/categories", json={"name": "Category to Delete"})
    category_id = response.json()["id"]

    delete_response = client.delete(f"/categories/{category_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/categories/{category_id}")
    assert get_response.status_code == 404
