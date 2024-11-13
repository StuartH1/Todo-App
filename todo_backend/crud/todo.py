from typing import Annotated, Any, Generator
import datetime as dt
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from database import engine
from schemas.todo import TodoCreate, Todo


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

def create_todo(todo: TodoCreate, session: Session = Depends(get_session)):
    db_todo = Todo(
        description=todo.description,
        due_date=todo.due_date,
        priority=todo.priority
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

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




