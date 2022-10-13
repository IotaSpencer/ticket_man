import random
from typing import Any, List

import sqlalchemy.engine
from sqlalchemy import delete, select, update
from sqlalchemy.engine import FrozenResult, Result, ResultProxy, Row, ScalarResult, \
    ChunkedIteratorResult
import arrow as arw
from ticket_man.db import session
from ticket_man.tables.tickets import TicketComments, TicketTypes, Tickets
from ticket_man.loggers import logger


def get_ticket_type(type_: int) -> sqlalchemy.engine.ScalarResult:
    with session() as sess:
        result: Result = sess.execute(select(TicketTypes).where(TicketTypes.id == type_))
        return result.scalars().first()


def submit_ticket(subject: str, content: str, type_: int, user_id: int) -> ResultProxy:
    with session() as sess:
        ticket = Tickets(subject=subject, content=content, type=type_, user_id=user_id, open=1, last_updated_by=user_id,
                         created=arw.now('US/Eastern').datetime, last_updated=arw.now('US/Eastern').datetime)
        sess.add(ticket)
        sess.commit()
    return ticket


def submit_comment(content: str, ticket_id: int, user_id: int) -> list[TicketComments | Any]:
    with session() as sess:
        comment = TicketComments(content=content, ticket_id=ticket_id, user_id=user_id)

        update_stmt = update(Tickets) \
            .where(Tickets.id == ticket_id) \
            .values(last_updated=arw.now('US/Eastern').datetime, last_updated_by=user_id)
        result = sess.execute(update_stmt)
        rows_updated = result.rowcount
        sess.add(comment)
        sess.commit()
    return [comment, rows_updated]


def get_all_user_tickets(user_id: int) -> ResultProxy:
    with session() as sess:
        result: Result = sess.execute(select(Tickets).where(Tickets.user_id == user_id))
        return result.scalars().all()


def get_all_ticket_types() -> ResultProxy:
    """Get all ticket types."""
    with session() as sess:
        result: Result = sess.execute(select(TicketTypes))
        return result.scalars().all()


def delete_comment(comment_id: int) -> ResultProxy | Result | FrozenResult:
    """Delete a comment."""
    with session() as sess:
        result: Result = sess.execute(select(TicketComments).where(TicketComments.id == comment_id))
        comment = result.freeze()
        sess.delete(comment)
        sess.commit()
        return comment


def close_ticket(ticket_id: int) -> ResultProxy | FrozenResult:
    """Close a ticket."""
    with session() as sess:
        result: Result = sess.execute(select(Tickets).where(Tickets.id == ticket_id))
        ticket = result.freeze()
        ticket.open = 0
        sess.commit()
        return ticket


def open_ticket(ticket_id: int) -> Result | FrozenResult:
    """Open a ticket."""
    with session() as sess:
        result: Result = sess.execute(select(Tickets).where(Tickets.id == ticket_id))
        ticket: FrozenResult = result.freeze()
        ticket.open = 1
        sess.commit()
        return ticket


def delete_ticket(ticket_id: int) -> bool:
    """Delete a ticket."""
    ticket_id = int(ticket_id)
    with session() as sess:
        result: Result = sess.execute(delete(Tickets).where(Tickets.id == ticket_id))

        sess.commit()
        return result.rowcount


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


def get_user_ticket(ticket_id: int, user_id: int) -> Result:
    """Get a ticket submitted by a user."""
    with session() as sess:
        result: Result = sess.execute(
                select(Tickets)
                .where(Tickets.user_id == user_id)
                .where(Tickets.id == ticket_id))
        return result


def get_ticket_comments(ticket_id: int) -> Result:
    with session() as sess:
        result: Result = sess.execute(select(TicketComments).where(TicketComments.ticket_id == ticket_id))
        return result


def get_ticket_comment(user_id: int, ticket_id: int, comment_id: int) -> ResultProxy | Result | FrozenResult:
    """Get a comment submitted by a user."""
    with session() as sess:
        result: Result = sess.execute(
                select(TicketComments).where(TicketComments.user_id == user_id).where(
                        TicketComments.id == comment_id).where(TicketComments.ticket_id == ticket_id))
        return result


def get_latest_ticket(user_id: int) -> Result | FrozenResult:
    """Get the latest ticket submitted by a user."""
    with session() as sess:
        result: Result = sess.execute(select(Tickets).
                                      where(Tickets.user_id == user_id).
                                      order_by(Tickets.id.desc()).
                                      limit(1))
        return result.freeze()


def get_last_5_tickets_by_user(user_id: int) -> list[Row]:
    """Get the last 5 tickets submitted by a user."""
    with session() as sess:
        result: ChunkedIteratorResult = sess.execute(
                select(Tickets)
                .where(Tickets.user_id == user_id)
                .order_by(Tickets.id.desc())
                .limit(5)
        )
        return result.all()


def close_latest_ticket(user_id: int) -> Result:
    """Close the latest ticket submitted by a user."""
    with session() as sess:
        result: Result = sess.execute(select(Tickets).where(Tickets.user_id == user_id).order_by(
                Tickets.id.desc()).limit(1))
        ticket = result.scalars().first()
        ticket.open = 0
        sess.commit()
        return ticket


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


def add_test_tickets():
    """Add test tickets to the database."""
    types = [1, 2, 3]
    numbers = '0123456789'
    with session() as sess:
        for i in range(100):
            user_id = int(''.join(random.choices(numbers, k=18)))
            type_ = random.choice(types)
            ticket = Tickets(subject=f"Test Ticket {i} + {type_}", content=f"Test Content {i}", type=type_,
                             user_id=user_id,
                             open=1)
            sess.add(ticket)

        sess.commit()
        return True
