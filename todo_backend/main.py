from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from crud.todo import create_todo
from schemas.todo import TodoCreate, Todo
from database import get_session
from fastapi import FastAPI

app = FastAPI()

@app.post("/todos", response_model=Todo)  # Return type
async def todo_creation(
    # What comes in from request body
    todo_data: TodoCreate,    
    # Database dependency
    db_session: Session = Depends(get_session)   
):
    return create_todo(todo=todo_data, session=db_session)

@app.get("/todos", response_model=List[Todo])
async def get_todos(db_session: Session = Depends(get_session)):
    todos = db_session.exec(select(Todo)).all()
    return todos

@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int, db_session: Session = Depends(get_session)):
    todo = db_session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(
    todo_id: int,
    todo_data: TodoCreate,
    db_session: Session = Depends(get_session)
):
    todo = db_session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo_data_dict = todo_data.dict(exclude_unset=True)
    for key, value in todo_data_dict.items():
        setattr(todo, key, value)
    
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)
    return todo

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db_session: Session = Depends(get_session)):
    todo = db_session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db_session.delete(todo)
    db_session.commit()
    return {"message": "Todo deleted successfully"}