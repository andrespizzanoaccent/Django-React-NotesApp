from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.note import Note
from backend.models.category import Category
from backend.schemas.note import NoteCreate, NoteUpdate

router = APIRouter()

@router.post('/notes/', response_model=Note)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    db_note = Note(title=note.title, content=note.content, category_id=note.category_id)
    db.add(db_note)
    try:
        db.commit()
        db.refresh(db_note)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return db_note

@router.put('/notes/{note_id}', response_model=Note)
def update_note(note_id: int, note: NoteUpdate, db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    for key, value in note.dict().items():
        setattr(db_note, key, value)
    try:
        db.commit()
        db.refresh(db_note)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return db_note

@router.get('/notes/', response_model=List[Note])
def read_notes(skip: int = 0, limit: int = 10, category_id: int = None, db: Session = Depends(get_db)):
    query = db.query(Note)
    if category_id:
        query = query.filter(Note.category_id == category_id)
    notes = query.offset(skip).limit(limit).all()
    return notes