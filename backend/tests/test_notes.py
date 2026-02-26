import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import get_db
from backend.models.note import Note
from backend.models.category import Category

client = TestClient(app)

def test_create_note_with_category(db: Session):
    category_response = client.post('/categories/', json={'name': 'Test Category', 'description': 'Test Description'})
    category_id = category_response.json()['id']
    response = client.post('/notes/', json={'title': 'Test Note', 'content': 'Test Content', 'category_id': category_id})
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == 'Test Note'
    assert data['category_id'] == category_id


def test_filter_notes_by_category(db: Session):
    category_response = client.post('/categories/', json={'name': 'Filter Category', 'description': 'Filter Description'})
    category_id = category_response.json()['id']
    client.post('/notes/', json={'title': 'Note 1', 'content': 'Content 1', 'category_id': category_id})
    client.post('/notes/', json={'title': 'Note 2', 'content': 'Content 2', 'category_id': category_id})
    response = client.get(f'/notes/?category_id={category_id}')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    for note in data:
        assert note['category_id'] == category_id