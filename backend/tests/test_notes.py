import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ..main import app
from ..database import get_db
from ..models import note as models
from ..schemas import note as schemas

client = TestClient(app)

def test_create_note_with_category(db: Session):
    category_response = client.post(
        "/categories/",
        json={"name": "Test Category", "description": "A test category"}
    )
    category_id = category_response.json()["id"]

    response = client.post(
        "/notes/",
        json={"title": "Test Note", "content": "This is a test note.", "category_id": category_id}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Note"
    assert data["category_id"] == category_id


def test_filter_notes_by_category(db: Session):
    category_response = client.post(
        "/categories/",
        json={"name": "Filter Category", "description": "Category for filtering"}
    )
    category_id = category_response.json()["id"]

    client.post(
        "/notes/",
        json={"title": "Note 1", "content": "Content 1", "category_id": category_id}
    )
    client.post(
        "/notes/",
        json={"title": "Note 2", "content": "Content 2", "category_id": category_id}
    )

    response = client.get(f"/notes/?category_id={category_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(note["category_id"] == category_id for note in data)
