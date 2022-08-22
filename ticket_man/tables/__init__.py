from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

# declarative base class
Base = declarative_base()

# an example mapping using the base
class Todo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True)
    content = Column(String)