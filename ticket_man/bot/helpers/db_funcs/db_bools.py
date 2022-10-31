from sqlalchemy import join, select
from sqlalchemy.engine import Result

from ticket_man.db import session
from ticket_man.loggers import logger
from ticket_man.tables.tickets import TicketComments, Tickets


def has_comments(ticket_id: int) -> bool:
    with session() as sess:
        result: Result = sess.execute(select(Tickets).where(Tickets.id == ticket_id).join(TicketComments, Tickets.id == TicketComments.ticket_id))
        return len(result.all()) > 0
