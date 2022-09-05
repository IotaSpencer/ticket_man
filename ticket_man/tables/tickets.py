from sqlalchemy import Column, ForeignKey, Integer, String

from ticket_man.tables.todo import Base


class Tickets(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    subject = Column(String)
    content = Column(String)
    type = Column(Integer), ForeignKey('ticket_types.id')  # 1 - bug, 2 - feature, 3 - support


class TicketTypes(Base):
    __tablename__ = 'ticket_types'

    id = Column(Integer, primary_key=True)
    desc = Column(String)
    type_name = Column(String)
