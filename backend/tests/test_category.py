import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from backend.main import app
from backend.database import get_db
from backend.models.category import Category
from backend.schemas.category import CategoryCreate

client = TestClient(app)

def test_create_category(db: Session):
    response = client.post("/api/categories/", json={"name": "Work", "description": "Work related tasks"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Work"
    assert data["description"] == "Work related tasks"

    # Test duplicate category creation
    response = client.post("/api/categories/", json={"name": "Work", "description": "Duplicate"})
    assert response.status_code == 400


def test_read_category(db: Session):
    category = Category(name="Personal", description="Personal tasks")
    db.add(category)
    db.commit()
    db.refresh(category)

    response = client.get(f"/api/categories/{category.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Personal"

    # Test non-existent category
    response = client.get("/api/categories/9999")
    assert response.status_code == 404
