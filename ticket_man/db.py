from os.path import expanduser
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import sessionmaker

from ticket_man.config import Configs
from ticket_man.tables import *

async def db():
    engine = create_async_engine(
        # In-memory sqlite database cannot be accessed from different
        # threads, use file.
        f'{expanduser(Configs.cfg.db.url)}')
    conn = await engine.connect()  # Insert some users
