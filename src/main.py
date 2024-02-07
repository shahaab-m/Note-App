from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from database import SessionLocal
import models
app = FastAPI()
db = SessionLocal()

class NoteBaseModal(BaseModel):
    class Config:
        orm_mode = True

class Note(NoteBaseModal):
    id: int
    author: str
    content: str

@app.get('/', response_model=list[Note], status_code=status.HTTP_200_OK)
def getAllNotes():
    allPosts = db.query(models.Note).all()
    return allPosts

@app.post('/create_note', response_model=Note, status_code=status.HTTP_201_CREATED)
def createNote(note:Note):
    newNote = models.Note(
        id = note.id,
        author = note.author,
        content = note.content
    )

    findNote = db.query(models.Note).filter(models.Note.id == note.id).first()

    if findNote is not None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Note with this id already exist")

    db.add(newNote)
    db.commit()

    return newNote

@app.put('/update_note/{noteId}', response_model=Note, status_code=status.HTTP_202_ACCEPTED)
def updateNote(noteId:int, note:Note):
    findNote = db.query(models.Note).filter(models.Note.id == note.id).first()
    findNote.id = note.id,
    findNote.author = note.author,
    findNote.content = note.content

    if findNote is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note with this id doesn't exist")

    db.commit()

    return findNote

@app.delete('/delete_note/{noteId}', response_model=Note, status_code=status.HTTP_200_OK)
def deleteNote(noteId:int, note:Note):
    findNoteToDelete = db.query(models.Note).filter(models.Note.id == note.id).first()
    db.delete(findNoteToDelete)

    if findNoteToDelete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note with this id doesn't exist")

    db.commit()

    return findNoteToDelete
