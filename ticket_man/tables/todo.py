from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Todo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    priority = Column(Integer)
    completed = Column(Integer)



