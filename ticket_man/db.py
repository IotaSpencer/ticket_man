from sqlalchemy_aio import ASYNCIO_STRATEGY
from os.path import expanduser

from sqlalchemy import (create_engine)
from sqlalchemy_aio import ASYNCIO_STRATEGY

from ticket_man.config import Configs
from ticket_man.tables import *

async def db():
    engine = create_engine(
        # In-memory sqlite database cannot be accessed from different
        # threads, use file.
        f'sqlite://{expanduser(Configs.cfg.db.path)}', strategy=ASYNCIO_STRATEGY)
    conn = await engine.connect()  # Insert some users
