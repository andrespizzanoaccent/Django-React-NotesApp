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
    # Create a category first
    category = Category(name='Note Test Category', description='Category for note test')
    db.add(category)
    db.commit()
    db.refresh(category)

    response = client.post('/api/notes/', json={'title': 'Test Note', 'content': 'Content of the test note', 'category_id': category.id})
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == 'Test Note'
    assert data['category_id'] == category.id


def test_filter_notes_by_category(db: Session):
    # Create categories
    category1 = Category(name='Category 1', description='First category')
    category2 = Category(name='Category 2', description='Second category')
    db.add(category1)
    db.add(category2)
    db.commit()
    db.refresh(category1)
    db.refresh(category2)

    # Create notes
    note1 = Note(title='Note 1', content='Content 1', category_id=category1.id)
    note2 = Note(title='Note 2', content='Content 2', category_id=category2.id)
    db.add(note1)
    db.add(note2)
    db.commit()

    response = client.get(f'/api/notes/?category_id={category1.id}')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['title'] == 'Note 1'
