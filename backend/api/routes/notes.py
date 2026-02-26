from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.note import Note
from backend.models.category import Category
from backend.schemas.note import NoteCreate, NoteUpdate

router = APIRouter()

@router.post("/notes/", response_model=Note)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == note.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    new_note = Note(title=note.title, content=note.content, category_id=note.category_id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@router.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: int, note: NoteUpdate, db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.category_id:
        category = db.query(Category).filter(Category.id == note.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        db_note.category_id = note.category_id
    db_note.title = note.title
    db_note.content = note.content
    db.commit()
    db.refresh(db_note)
    return db_note
