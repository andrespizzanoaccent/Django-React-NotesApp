import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from backend.main import app
from backend.database import get_db
from backend.models.note import Note
from backend.models.category import Category
from backend.schemas.note import NoteCreate

client = TestClient(app)

def test_create_note_with_category(db: Session):
    category = Category(name="Work", description="Work related tasks")
    db.add(category)
    db.commit()
    db.refresh(category)

    response = client.post("/api/notes/", json={"title": "Meeting notes", "content": "Discuss project milestones", "category_id": category.id})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Meeting notes"
    assert data["category_id"] == category.id

    # Test with non-existent category
    response = client.post("/api/notes/", json={"title": "Invalid category", "content": "This should fail", "category_id": 9999})
    assert response.status_code == 404
