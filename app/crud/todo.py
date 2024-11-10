# CREATE TABLE todos (
#     id SERIAL PRIMARY KEY,
#     description TEXT,
#     is_completed BOOLEAN DEFAULT FALSE,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     due_date TIMESTAMP,
#     priority VARCHAR(20) CHECK (priority IN ('Low', 'Medium', 'High'))
# );


from typing import Annotated, Any, Generator
import datetime as dt
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.database import engine

class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    description: str = Field(index=True)
    is_completed: bool = Field(default=False)
    created_at: dt.datetime = Field(default=dt.datetime.now())
    updated_at: dt.datetime = Field(default=dt.datetime.now())
    due_date: dt.datetime | None = Field(default=None)
    priority: str = Field(default="Low")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session

def create_todo(todo: Todo, session: Session = Depends(get_session)):
    session.add(todo)
    session.commit()

def get_todos(session: Session = Depends(get_session)):
    return session.exec(select(Todo)).all()

def get_todo(id: int, session: Session = Depends(get_session)):
    return session.get(Todo, id)

def update_todo(todo: Todo, session: Session = Depends(get_session)):
    session.add(todo)
    session.commit()

def delete_todo(id: int, session: Session = Depends(get_session)):
    todo = session.get(Todo, id)
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo with id {id} not found")
    session.delete(todo)
    session.commit()




