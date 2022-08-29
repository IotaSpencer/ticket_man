from sqlalchemy import Column, Integer, String

from ticket_man.tables import Base


class Todo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    priority = Column(Integer)
    completed = Column(Integer)
