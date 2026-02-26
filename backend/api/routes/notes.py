from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from ..models import note as models
from ..schemas import note as schemas
from ..database import get_db

router = APIRouter()

@router.post("/notes/", response_model=schemas.Note)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_note = models.Note(title=note.title, content=note.content, category_id=note.category_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/notes/", response_model=List[schemas.Note])
def read_notes(skip: int = 0, limit: int = 10, category_id: int = None, db: Session = Depends(get_db)):
    query = db.query(models.Note)
    if category_id is not None:
        query = query.filter(models.Note.category_id == category_id)
    notes = query.offset(skip).limit(limit).all()
    return notes

@router.put("/notes/{note_id}", response_model=schemas.Note)
def update_note(note_id: int, note: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    db_note.title = note.title
    db_note.content = note.content
    db_note.category_id = note.category_id
    db.commit()
    db.refresh(db_note)
    return db_note
