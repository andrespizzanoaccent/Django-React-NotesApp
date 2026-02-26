import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ..main import app
from ..database import get_db
from ..models import category as models
from ..schemas import category as schemas

client = TestClient(app)

def test_create_category(db: Session):
    response = client.post(
        "/categories/",
        json={"name": "Work", "description": "Work related notes"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Work"
    assert data["description"] == "Work related notes"


def test_read_categories(db: Session):
    response = client.get("/categories/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_update_category(db: Session):
    response = client.post(
        "/categories/",
        json={"name": "Personal", "description": "Personal notes"}
    )
    category_id = response.json()["id"]

    update_response = client.put(
        f"/categories/{category_id}",
        json={"name": "Updated Personal", "description": "Updated description"}
    )
    assert update_response.status_code == 200
    update_data = update_response.json()
    assert update_data["name"] == "Updated Personal"


def test_delete_category(db: Session):
    response = client.post(
        "/categories/",
        json={"name": "Temporary", "description": "Temporary category"}
    )
    category_id = response.json()["id"]

    delete_response = client.delete(f"/categories/{category_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/categories/{category_id}")
    assert get_response.status_code == 404
