from sqlalchemy import Column, ForeignKey, Integer, String, Table

from ticket_man import db
from ticket_man.utils import Base


class Todo(Base):
    __table__ = Table(
            'todo',
            Base.metadata,
            Column('id', Integer, primary_key=True),
            Column('content', String),
            Column('priority', Integer),
            Column('completed', Integer),
            autoload_with=db.db_engine
    )
