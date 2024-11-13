from typing import Any, Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

from sqlmodel import Session
SQLALCHEMY_DATABASE_URL = "postgresql://stu:@localhost:5432/todo_app"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_session() -> Generator[Session, Any, None]:
    with SessionLocal() as session:
        yield session