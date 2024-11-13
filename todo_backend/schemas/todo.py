from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic import Field
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    due_date: Optional[datetime] = None
    priority: Optional[str] = "Low"

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass

class TodoDelete(BaseModel):
    id: int = Field(description="The ID of the todo to delete")



class Todo(TodoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True