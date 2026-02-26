import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import get_db
from backend.models.category import Category

client = TestClient(app)

def test_create_category(db: Session):
    response = client.post('/categories/', json={'name': 'Work', 'description': 'Work related tasks'})
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Work'
    assert data['description'] == 'Work related tasks'


def test_read_categories(db: Session):
    response = client.get('/categories/')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_update_category(db: Session):
    response = client.post('/categories/', json={'name': 'Personal', 'description': 'Personal tasks'})
    category_id = response.json()['id']
    response = client.put(f'/categories/{category_id}', json={'name': 'Personal Updated', 'description': 'Updated description'})
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Personal Updated'
    assert data['description'] == 'Updated description'


def test_delete_category(db: Session):
    response = client.post('/categories/', json={'name': 'Temporary', 'description': 'To be deleted'})
    category_id = response.json()['id']
    response = client.delete(f'/categories/{category_id}')
    assert response.status_code == 200
    response = client.get(f'/categories/{category_id}')
    assert response.status_code == 404