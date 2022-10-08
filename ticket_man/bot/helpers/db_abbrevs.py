import random
from typing import Any, List

import sqlalchemy.engine
from sqlalchemy import delete, select, update
from sqlalchemy.engine import FrozenResult, LegacyCursorResult, Result, ResultProxy, Row, ScalarResult, \
    ChunkedIteratorResult
import arrow as arw
from ticket_man.db import async_session
from ticket_man.tables.tickets import TicketComments, TicketTypes, Tickets
from ticket_man.loggers import logger


async def get_ticket_type(type_: int) -> sqlalchemy.engine.ScalarResult:
    async with async_session() as session:
        result: Result = await session.execute(select(TicketTypes).where(TicketTypes.id == type_))
        return result.scalars().first()


async def submit_ticket(subject: str, content: str, type_: int, user_id: int) -> ResultProxy:
    async with async_session() as session:
        ticket = Tickets(subject=subject, content=content, type=type_, user_id=user_id, open=1, last_updated_by=user_id, created=arw.now('US/Eastern').datetime, last_updated=arw.now('US/Eastern').datetime)
        session.add(ticket)
        await session.commit()
        return ticket


async def submit_comment(content: str, ticket_id: int, user_id: int) -> list[TicketComments | Any]:
    async with async_session() as session:
        comment = TicketComments(content=content, ticket_id=ticket_id, user_id=user_id)

        update_stmt = update(Tickets)\
            .where(Tickets.id == ticket_id)\
            .values(last_updated=arw.now('US/Eastern').datetime, last_updated_by=user_id)
        result = await session.execute(update_stmt)
        rows_updated = result.rowcount
        session.add(comment)
        await session.commit()
        return [comment, rows_updated]


async def get_all_user_tickets(user_id: int) -> ResultProxy:
    async with async_session() as session:
        result: Result = await session.execute(select(Tickets).where(Tickets.user_id == user_id))
        return result.scalars().all()


async def get_all_ticket_types() -> ResultProxy:
    """Get all ticket types."""
    async with async_session() as session:
        result: Result = await session.execute(select(TicketTypes))
        return result.scalars().all()


async def delete_comment(comment_id: int) -> ResultProxy | Result | FrozenResult:
    """Delete a comment."""
    async with async_session() as session:
        result: Result = await session.execute(select(TicketComments).where(TicketComments.id == comment_id))
        comment = result.freeze()
        await session.delete(comment)
        await session.commit()
        return comment


async def close_ticket(ticket_id: int) -> ResultProxy | FrozenResult:
    """Close a ticket."""
    async with async_session() as session:
        result: Result = await session.execute(select(Tickets).where(Tickets.id == ticket_id))
        ticket = result.freeze()
        ticket.open = 0
        await session.commit()
        return ticket


async def open_ticket(ticket_id: int) -> Result | FrozenResult:
    """Open a ticket."""
    async with async_session() as session:
        result: Result = await session.execute(select(Tickets).where(Tickets.id == ticket_id))
        ticket: FrozenResult = result.freeze()
        ticket.open = 1
        await session.commit()
        return ticket


async def delete_ticket(ticket_id: int) -> bool:
    """Delete a ticket."""
    ticket_id = int(ticket_id)
    async with async_session() as session:
        result: Result = await session.execute(delete(Tickets).where(Tickets.id == ticket_id))

        await session.commit()
        return result.rowcount


async def get_ticket(ticket_id: int) -> Result:
    logger.info(f"Getting ticket {ticket_id}")
    logger.info(f"Expression: {select(Tickets).where(Tickets.id == ticket_id)}")
    async with async_session() as session:
        logger.info(f"Session: {session}")
        result: Result = await session.execute(select(Tickets).where(Tickets.id == ticket_id))
        return result


async def get_ticket_comment_by_id(comment_id: int) -> Result:
    async with async_session() as session:
        result: Result = await session.execute(select(TicketComments).where(TicketComments.id == comment_id))
        return result


async def get_user_ticket(ticket_id: int, user_id: int) -> Result:
    """Get a ticket submitted by a user."""
    async with async_session() as session:
        result: Result = await session.execute(
                select(Tickets)
                .where(Tickets.user_id == user_id)
                .where(Tickets.id == ticket_id))
        return result


async def get_ticket_comments(ticket_id: int) -> Result:
    async with async_session() as session:
        result: Result = await session.execute(select(TicketComments).where(TicketComments.ticket_id == ticket_id))
        return result


async def get_ticket_comment(user_id: int, ticket_id: int, comment_id: int) -> ResultProxy | Result | FrozenResult:
    """Get a comment submitted by a user."""
    async with async_session() as session:
        result: Result = await session.execute(
                select(TicketComments).where(TicketComments.user_id == user_id).where(
                        TicketComments.id == comment_id).where(TicketComments.ticket_id == ticket_id))
        return result


async def get_latest_ticket(user_id: int) -> Result | FrozenResult:
    """Get the latest ticket submitted by a user."""
    async with async_session() as session:
        result: Result = await session.execute(select(Tickets).
                                               where(Tickets.user_id == user_id).
                                               order_by(Tickets.id.desc()).
                                               limit(1))
        return result.freeze()


async def get_last_5_tickets_by_user(user_id: int) -> list[Row]:
    """Get the last 5 tickets submitted by a user."""
    async with async_session() as session:
        result: ChunkedIteratorResult = await session.execute(
            select(Tickets)
            .where(Tickets.user_id == user_id)
            .order_by(Tickets.id.desc())
            .limit(5)
        )
        return result.all()


async def close_latest_ticket(user_id: int) -> Result:
    """Close the latest ticket submitted by a user."""
    async with async_session() as session:
        result: Result = await session.execute(select(Tickets).where(Tickets.user_id == user_id).order_by(
                Tickets.id.desc()).limit(1))
        ticket = result.scalars().first()
        ticket.open = 0
        await session.commit()
        return ticket


async def get_latest_comment(user_id: int) -> Result:
    """Get the latest comment submitted by a user."""
    async with async_session() as session:
        result: Result = await session.execute(
                select(TicketComments).where(TicketComments.user_id == user_id).order_by(
                        TicketComments.id.desc()).limit(1))
        return result


async def get_all_open_tickets() -> FrozenResult | LegacyCursorResult | Result:
    """Get all open tickets."""
    async with async_session() as session:
        result: Result = await session.execute(select(Tickets).where(Tickets.open == 1))
        return result.scalars().all()


async def get_all_tickets() -> ResultProxy:
    """Get all tickets."""
    async with async_session() as session:
        result: Result = await session.execute(select(Tickets))
        return result.scalars().all()


async def get_all_comments(user_id: int) -> ResultProxy:
    """Get all comments submitted by a user."""
    async with async_session() as session:
        result: Result = await session.execute(select(TicketComments).where(TicketComments.user_id == user_id))
        return result.scalars().all()


async def get_all_ticket_comments(user_id: int, ticket_id: int) -> ResultProxy:
    """Get all comments submitted by a user on a ticket."""
    async with async_session() as session:
        result: Result = await session.execute(
                select(TicketComments).where(TicketComments.ticket_id == ticket_id).where(
                        TicketComments.user_id == user_id))
        return result.scalars().all()


async def add_test_tickets():
    """Add test tickets to the database."""
    types = [1, 2, 3]
    numbers = '0123456789'
    async with async_session() as session:
        for i in range(100):
            user_id = int(''.join(random.choices(numbers, k=18)))
            type_ = random.choice(types)
            ticket = Tickets(subject=f"Test Ticket {i} + {type_}", content=f"Test Content {i}", type=type_,
                             user_id=user_id,
                             open=1)
            session.add(ticket)

        await session.commit()
        return True
