from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ticket_man.utils import Base


class Tickets(Base):
    __tablename__ = 'tickets'
    autoload_with = Base.metadata.bind
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    open = Column(Integer)  # 0 - closed, 1 - open
    subject = Column(String)
    content = Column(String)
    created = Column(DateTime)  #
    last_updated = Column(DateTime)  # last comment
    last_updated_by = Column(Integer)  # user_id
    type = Column(Integer, ForeignKey('ticket_types.id'))  # 1 - bug, 2 - feature, 3 - support
    comments = relationship('TicketComments', primaryjoin='Tickets.id==TicketComments.ticket_id',
                            order_by='TicketComments.timestamp', back_populates='ticket')


class TicketTypes(Base):
    __tablename__ = 'ticket_types'

    id = Column(Integer, primary_key=True)
    desc = Column(String)
    type_name = Column(String)


class TicketComments(Base):
    __tablename__ = 'ticket_comments'

    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey('tickets.id'))
    timestamp = Column(DateTime)
    user_id = Column(Integer)
    content = Column(String)
    ticket = relationship('Tickets', back_populates='comments')
