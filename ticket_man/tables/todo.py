from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Todo(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    priority = Column(Integer)
    completed = Column(Integer)


class Tickets(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    type = Column(Integer), ForeignKey('ticket_types.id')  # 1 - bug, 2 - feature, 3 - support


class Types(Base):
    __tablename__ = 'types'

    id = Column(Integer, primary_key=True)
    desc = Column(String)
    type_name = Column(String)
