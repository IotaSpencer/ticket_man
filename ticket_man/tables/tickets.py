from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ticket_man.tables.todo import Base


class Tickets(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    subject = Column(String)
    content = Column(String)
    type = Column(Integer), ForeignKey('ticket_types.id')  # 1 - bug, 2 - feature, 3 - support
    comments = relationship('Comments', back_populates='ticket_comments')

class TicketTypes(Base):
    __tablename__ = 'ticket_types'

    id = Column(Integer, primary_key=True)
    desc = Column(String)
    type_name = Column(String)


class TicketComments(Base):
    __tablename__ = 'ticket_comments'

    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer), ForeignKey('tickets.id')
    datetime = Column(DateTime)
    content = Column(String)

    ticket = relationship('Ticket', back_populates='comments')
