from typing import Any

from sqlalchemy.orm import Session

import arrow as arw
from sqlalchemy import delete, update
from sqlalchemy.engine import FrozenResult, Result, ResultProxy
from sqlalchemy.future import select

from ticket_man.db import session
from ticket_man.tables.tickets import TicketComments, Tickets


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


def delete_comment(comment_id: int) -> ResultProxy | Result | FrozenResult:
    """Delete a comment."""
    with session() as sess:
        result: Result = sess.execute(select(TicketComments).where(TicketComments.id == comment_id))
        comment = result.freeze()
        sess.delete(comment)
        sess.commit()
        return comment


def close_ticket(ticket_id: int) -> bool:
    """Close a ticket."""
    with session() as sess:  # type: Session
        ticket = sess.execute(update(Tickets).where(Tickets.id == ticket_id).values(open=0))
        sess.commit()
        return True


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


def close_latest_ticket(user_id: int) -> Result:
    """Close the latest ticket submitted by a user."""
    with session() as sess:
        result: Result = sess.execute(select(Tickets).where(Tickets.user_id == user_id).order_by(
                Tickets.id.desc()).limit(1))
        ticket = result.scalars().first()
        ticket.open = 0
        sess.commit()
        return ticket
