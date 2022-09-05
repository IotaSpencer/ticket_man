import sqlalchemy.engine
from sqlalchemy import select
from sqlalchemy.engine import Result, ResultProxy

from ticket_man.db import async_session
from ticket_man.tables.tickets import TicketTypes, Tickets
from ticket_man.loggers import logger


async def get_ticket_type(type_: int) -> sqlalchemy.engine.ScalarResult:
    async with async_session() as session:
        result: Result = await session.execute(select(TicketTypes).where(TicketTypes.id == type_))
        return result.scalars().first()
