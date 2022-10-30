from sqlalchemy import join, select

from ticket_man.db import session
from ticket_man.tables.tickets import TicketComments, Tickets


def has_comments(ticket_id: int) -> bool:
    with session() as sess:
        sess.execute(select(TicketComments.))
