from sqlalchemy import join, select

from ticket_man.db import session
from ticket_man.loggers import logger
from ticket_man.tables.tickets import TicketComments, Tickets


def has_comments(ticket_id: int) -> bool:
    with session() as sess:
        result = sess.execute(select(TicketComments.comments).where(TicketComments.ticket_id == ticket_id))
        logger.info(result.scalars().all())
