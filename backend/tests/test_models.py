import pytest
from sqlalchemy.exc import IntegrityError
from backend.models.category import Category
from backend.database import SessionLocal

@pytest.fixture
def db_session():
    session = SessionLocal()
    yield session
    session.close()

def test_create_category(db_session):
    category = Category(name='Test Category')
    db_session.add(category)
    db_session.commit()
    assert category.id is not None

    fetched_category = db_session.query(Category).filter_by(name='Test Category').first()
    assert fetched_category is not None
    assert fetched_category.name == 'Test Category'


def test_create_duplicate_category(db_session):
    category1 = Category(name='Duplicate Category')
    db_session.add(category1)
    db_session.commit()

    category2 = Category(name='Duplicate Category')
    db_session.add(category2)
    with pytest.raises(IntegrityError):
        db_session.commit()
