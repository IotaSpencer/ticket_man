import sqlalchemy
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from ticket_man.utils import Base
from ticket_man import db


class Tickets(Base):
    __table__ = Table(
            'tickets',
            Base.metadata,
            Column('id', Integer, primary_key=True),
            Column("user_id", Integer),
            Column("open", Integer),  # 0 - closed, 1 - open
            Column("subject", String(255)),
            Column("content", String(255)),
            Column("type", Integer, ForeignKey("ticket_types.id")),
            Column("last_updated_by", Integer),  # user_id
            Column("created", DateTime),
            Column("last_updated", DateTime),  # last comment

            autoload_with=db.db_engine,

    )

    comments = relationship('TicketComments', primaryjoin='Tickets.id==TicketComments.ticket_id',
                            order_by='TicketComments.timestamp', back_populates='ticket')


class TicketTypes(Base):
    __table__ = Table(
            'ticket_types',
            Base.metadata,
            Column('id', Integer, primary_key=True),
            Column('desc', String),
            Column('type_name', String),
            autoload_with=db.db_engine,
    )


class TicketComments(Base):
    __table__ = Table(
            'ticket_comments',
            Base.metadata,
            Column('id', Integer, primary_key=True),
            Column('ticket_id', Integer, ForeignKey('tickets.id')),
            Column('timestamp', DateTime),
            Column('user_id', Integer),
            Column('content', String),
            autoload_with=db.db_engine,
    )
    ticket = relationship('Tickets', back_populates='comments')
