import sqlalchemy
from sqlalchemy import select
from sqlalchemy.engine import ChunkedIteratorResult, FrozenResult, Result, ResultProxy, Row

from ticket_man.db import session
from ticket_man.loggers import logger
from ticket_man.tables.tickets import TicketComments, TicketTypes, Tickets


def get_latest_comment(user_id: int) -> Result:
    """Get the latest comment submitted by a user."""
    with session() as sess:
        result: Result = sess.execute(
                select(TicketComments).where(TicketComments.user_id == user_id).order_by(
                        TicketComments.id.desc()).limit(1))
        return result


def get_all_open_tickets() -> FrozenResult | Result:
    """Get all open tickets."""
    with session() as sess:
        result: Result = sess.execute(select(Tickets).where(Tickets.open == 1))
        return result.scalars().all()


def get_all_user_open_tickets(user_id: int) -> FrozenResult | Result:
    """Get all open tickets submitted by a user."""
    with session() as sess:
        result: Result = sess.execute(
                select(Tickets).where(Tickets.user_id == user_id).where(Tickets.open == 1))
        return result.scalars().all()


def get_all_tickets() -> ResultProxy:
    """Get all tickets."""
    with session() as sess:
        result: Result = sess.execute(select(Tickets))
        return result.scalars().all()


def get_all_comments(user_id: int) -> ResultProxy:
    """Get all comments submitted by a user."""
    with session() as sess:
        result: Result = sess.execute(select(TicketComments).where(TicketComments.user_id == user_id))
        return result.scalars().all()


def get_all_ticket_comments(user_id: int, ticket_id: int) -> ResultProxy:
    """Get all comments submitted by a user on a ticket."""
    with session() as sess:
        result: Result = sess.execute(
                select(TicketComments).where(TicketComments.ticket_id == ticket_id).where(
                        TicketComments.user_id == user_id))
        return result.scalars().all()


def get_ticket(ticket_id: int) -> Result:
    logger.info(f"Getting ticket {ticket_id}")
    logger.info(f"Expression: {select(Tickets).where(Tickets.id == ticket_id)}")
    with session() as sess:
        logger.info(f"Session: {session}")
        result: Result = sess.execute(select(Tickets).where(Tickets.id == ticket_id))
        return result


def get_ticket_comment_by_id(comment_id: int) -> Result:
    with session() as sess:
        result: Result = sess.execute(select(TicketComments).where(TicketComments.id == comment_id))
        return result


def get_user_ticket(ticket_id: int, user_id: int) -> list:
    """Get a ticket submitted by a user."""
    with session() as sess:
        result: Result = sess.execute(
                select(Tickets)
                .where(Tickets.user_id == user_id)
                .where(Tickets.id == ticket_id))
        return result.scalars().all()


def get_ticket_comments(ticket_id: int) -> FrozenResult:
    with session() as sess:
        result: Result = sess.execute(select(TicketComments).where(TicketComments.ticket_id == ticket_id))
        return result.freeze()


def get_ticket_comment(user_id: int, ticket_id: int, comment_id: int) -> ResultProxy | Result | FrozenResult:
    """Get a comment submitted by a user."""
    with session() as sess:
        result: Result = sess.execute(
                select(TicketComments).where(TicketComments.user_id == user_id).where(
                        TicketComments.id == comment_id).where(TicketComments.ticket_id == ticket_id))
        return result


def get_latest_ticket(user_id: int):
    """Get the latest open ticket submitted by a user."""
    with session() as sess:
        result = sess.execute(
                select(Tickets).
                where(Tickets.user_id == user_id).
                where(Tickets.open == 1).
                order_by(Tickets.id.desc()).
                limit(1))
        return result.scalars().first()


def get_ticket_type(type_: int) -> sqlalchemy.engine.ScalarResult:
    with session() as sess:
        result: Result = sess.execute(select(TicketTypes).where(TicketTypes.id == type_))
        return result.scalars().first()


def get_last_5_tickets_by_user(user_id: int) -> list[Row]:
    """Get the last 5 tickets submitted by a user."""
    with session() as sess:
        result: ChunkedIteratorResult = sess.execute(
                select(Tickets)
                .where(Tickets.user_id == user_id)
                .order_by(Tickets.id.desc())
                .limit(5)
        )
        return result.scalars().all()


def get_all_user_tickets(user_id: int) -> ResultProxy:
    with session() as sess:
        result: Result = sess.execute(select(Tickets).where(Tickets.user_id == user_id))
        return result.scalars().all()


def get_all_ticket_types() -> ResultProxy:
    """Get all ticket types."""
    with session() as sess:
        result: Result = sess.execute(select(TicketTypes))
        return result.scalars().all()
