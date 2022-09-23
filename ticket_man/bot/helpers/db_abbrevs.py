import random

import sqlalchemy.engine
from sqlalchemy import delete, select
from sqlalchemy.engine import LegacyCursorResult, Result, ResultProxy, Row, ScalarResult

from ticket_man.db import async_session
from ticket_man.tables.tickets import TicketComments, TicketTypes, Tickets
from ticket_man.loggers import logger


async def get_ticket_type(type_: int) -> sqlalchemy.engine.ScalarResult:
    async with async_session() as session:
        result: Result = await session.execute(select(TicketTypes).where(TicketTypes.id == type_))
        return result.scalars().first()


async def submit_ticket(subject: str, content: str, type_: int, user_id: int) -> ResultProxy:
    async with async_session() as session:
        ticket = Tickets(subject=subject, content=content, type=type_, user_id=user_id, open=1)
        session.add(ticket)
        await session.commit()
        return ticket


async def submit_comment(content: str, ticket_id: int, user_id: int) -> ResultProxy:
    async with async_session() as session:
        comment = TicketComments(content=content, ticket_id=ticket_id, user_id=user_id)
        session.add(comment)
        await session.commit()
        return comment


async def get_all_user_tickets(user_id: int) -> ResultProxy:
    async with async_session() as session:
        result: Result = await session.execute(select(Tickets).where(Tickets.user_id == user_id))
        return result.scalars().all()


async def get_all_ticket_types() -> ResultProxy:
    """Get all ticket types."""
    async with async_session() as session:
        result: Result = await session.execute(select(TicketTypes))
        return result.scalars().all()


async def delete_comment(comment_id: int) -> ResultProxy:
    """Delete a comment."""
    async with async_session() as session:
        result: Result = await session.execute(select(TicketComments).where(TicketComments.id == comment_id))
        comment = result.scalars().first()
        await session.delete(comment)
        await session.commit()
        return comment


async def close_ticket(ticket_id: int) -> ResultProxy:
    """Close a ticket."""
    async with async_session() as session:
        result: Result = await session.execute(select(Tickets).where(Tickets.id == ticket_id))
        ticket = result.scalars().first()
        ticket.open = 0
        await session.commit()
        return ticket


async def open_ticket(ticket_id: int) -> ResultProxy:
    """Open a ticket."""
    async with async_session() as session:
        result: Result = await session.execute(select(Tickets).where(Tickets.id == ticket_id))
        ticket = result.scalars().first()
        ticket.open = 1
        await session.commit()
        return ticket


async def delete_ticket(ticket_id: int) -> Result:
    """Delete a ticket."""
    ticket_id = int(ticket_id)
    async with async_session() as session:
        result: Result = await session.execute(delete(Tickets).where(Tickets.id == ticket_id))
        ticket: Result = result
        await session.commit()
        return ticket


async def get_ticket(ticket_id: int) -> Row | None:
    logger.info(f"Getting ticket {ticket_id}")
    logger.info(f"Expression: {select(Tickets).where(Tickets.id == ticket_id)}")
    async with async_session() as session:
        logger.info(f"Session: {session}")
        result: Result = await session.execute(select(Tickets).where(Tickets.id == ticket_id))
        return result.scalars().first()


async def get_ticket_comments(ticket_id: int) -> ResultProxy:
    async with async_session() as session:
        result: Result = await session.execute(select(TicketComments).where(TicketComments.ticket_id == ticket_id))
        return result.scalars().all()


async def get_ticket_comment(user_id: int, ticket_id: int, comment_id: int) -> ResultProxy:
    """Get a comment submitted by a user."""
    async with async_session() as session:
        result: Result = await session.execute(
                select(TicketComments).where(TicketComments.user_id == user_id).where(
                        TicketComments.id == comment_id).where(TicketComments.ticket_id == ticket_id))
        return result.scalars().first()


async def get_latest_ticket(user_id: int) -> ResultProxy:
    """Get the latest ticket submitted by a user."""
    async with async_session() as session:
        result: Result = await session.execute(select(Tickets).
                                               where(Tickets.user_id == user_id).
                                               order_by(Tickets.id.desc()).
                                               limit(1))
        return result.scalars().first()


async def close_latest_ticket(user_id: int) -> ResultProxy:
    """Close the latest ticket submitted by a user."""
    async with async_session() as session:
        result: Result = await session.execute(select(Tickets).where(Tickets.user_id == user_id).order_by(
                Tickets.id.desc()).limit(1))
        ticket = result.scalars().first()
        ticket.open = 0
        await session.commit()
        return ticket


async def get_latest_comment(user_id: int) -> ResultProxy:
    """Get the latest comment submitted by a user."""
    async with async_session() as session:
        result: Result = await session.execute(
                select(TicketComments).where(TicketComments.user_id == user_id).order_by(
                        TicketComments.id.desc()).limit(1))
        return result.scalars().first()


async def get_all_open_tickets() -> ResultProxy:
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
    tickets = []
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
