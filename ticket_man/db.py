from os.path import expanduser
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import sessionmaker

from ticket_man.config import Configs
from ticket_man.tables import *

dbcfg = Configs.cfg.db

async def db():
    """
    :rtype: Connection
    """
    engine = create_async_engine(f'{dbcfg.proto}://{dbcfg.user}:{dbcfg.password}@{dbcfg.host}/{dbcfg.database}?charset=utf8mb4')
    conn = await engine.connect()  # type: Connection
    return conn
