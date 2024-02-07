from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Note(BaseModel):
    id: int
    author: str
    content: str


@app.get('/', status_code=200)
def getNoteInfo():
    return {"message": "server is running"}


@app.get('/getNoteById/{note_id}', status_code=200)
def getNoteById(note_id: int):
    return {"message": f"Your Note Id is {note_id}"}


@app.post('/addNote', status_code=200)
def addNote(note: Note):
    return {
        "id": note.id,
        "author": note.author,
        "content": note.content
    }
