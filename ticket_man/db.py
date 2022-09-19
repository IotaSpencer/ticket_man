import asyncio
from asyncio import current_task

from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import sessionmaker

from ticket_man.config import Configs
from ticket_man.tables.todo import *
from ticket_man.tables.tickets import *

dbcfg = Configs.cfg.db
db_engine = create_async_engine(
    f'{dbcfg.proto}://{dbcfg.user}:{dbcfg.password}@{dbcfg.host}/{dbcfg.database}?charset=utf8mb4&read_timeout=30&write_timeout=30&connect_timeout=30', echo=True)

async_session = async_scoped_session(sessionmaker(db_engine, expire_on_commit=False, class_=AsyncSession), scopefunc=current_task)
