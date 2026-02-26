from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models.note import Note
from backend.models.category import Category
from backend.schemas.note import NoteCreate, NoteRead

router = APIRouter()

@router.post('/', response_model=NoteRead)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == note.category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db_note = Note(title=note.title, content=note.content, category_id=note.category_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get('/', response_model=List[NoteRead])
def read_notes(skip: int = 0, limit: int = 10, category_id: int = None, db: Session = Depends(get_db)):
    query = db.query(Note)
    if category_id is not None:
        query = query.filter(Note.category_id == category_id)
    notes = query.offset(skip).limit(limit).all()
    return notes

@router.put('/{note_id}', response_model=NoteRead)
def update_note(note_id: int, note: NoteCreate, db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    db_category = db.query(Category).filter(Category.id == note.category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db_note.title = note.title
    db_note.content = note.content
    db_note.category_id = note.category_id
    db.commit()
    db.refresh(db_note)
    return db_note
