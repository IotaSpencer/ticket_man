import sqlalchemy.engine
from sqlalchemy import select
from sqlalchemy.engine import Result, ResultProxy

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


async def get_ticket(ticket_id: int) -> ResultProxy:
    async with async_session() as session:
        result: Result = await session.execute(select(Tickets).where(Tickets.id == ticket_id))
        return result.scalars().first()


async def get_ticket_comments(ticket_id: int) -> ResultProxy:
    async with async_session() as session:
        result: Result = await session.execute(select(TicketComments).where(TicketComments.ticket_id == ticket_id))
        return result.scalars().all()


async def get_ticket_comment(user_id: int, comment_id: int) -> ResultProxy:
    async with async_session() as session:
        result: Result = await session.execute(
            select(TicketComments).where(TicketComments.user_id == user_id).where(TicketComments.id == comment_id))
        return result.scalars().first()


async def get_latest_ticket(user_id: int) -> ResultProxy:
    async with async_session() as session:
        result: Result = await session.execute(select(Tickets).order_by(Tickets.id.desc()).limit(1))
        return result.scalars().first()


async def get_latest_comment(user_id: int) -> ResultProxy:
    async with async_session() as session:
        result: Result = await session.execute(
            select(TicketComments).where(TicketComments.user_id == user_id).order_by(TicketComments.id.desc()).limit(1))
        return result.scalars().first()


async def get_all_tickets() -> ResultProxy:
    async with async_session() as session:
        result: Result = await session.execute(select(Tickets))
        return result.scalars().all()


async def get_all_comments(user_id: int) -> ResultProxy:
    async with async_session() as session:
        result: Result = await session.execute(select(TicketComments).where(TicketComments.user_id == user_id))
        return result.scalars().all()


async def get_all_ticket_comments(ticket_id: int) -> ResultProxy:
    async with async_session() as session:
        result: Result = await session.execute(select(TicketComments).where(TicketComments.ticket_id == ticket_id))
        return result.scalars().all()
