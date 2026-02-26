import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.main import app
from backend.database import get_db
from backend.models.category import Category
from backend.schemas.category import CategoryCreate

client = TestClient(app)

def test_create_category(db: Session):
    response = client.post('/api/categories/', json={'name': 'Test Category', 'description': 'A test category'})
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Test Category'
    assert data['description'] == 'A test category'


def test_read_categories(db: Session):
    response = client.get('/api/categories/')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_update_category(db: Session):
    # Create a category first
    category = Category(name='Update Test', description='Update test category')
    db.add(category)
    db.commit()
    db.refresh(category)

    response = client.put(f'/api/categories/{category.id}', json={'name': 'Updated Category', 'description': 'Updated description'})
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Updated Category'
    assert data['description'] == 'Updated description'


def test_delete_category(db: Session):
    # Create a category first
    category = Category(name='Delete Test', description='Delete test category')
    db.add(category)
    db.commit()
    db.refresh(category)

    response = client.delete(f'/api/categories/{category.id}')
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Delete Test'

    # Ensure it's deleted
    response = client.get(f'/api/categories/{category.id}')
    assert response.status_code == 404
