import asyncio
from sqlalchemy_aio import ASYNCIO_STRATEGY
from sqlalchemy import (Column, Integer, MetaData, Table, Text, create_engine, select)
from sqlalchemy.schema import CreateTable, DropTable
from ticket_man.config import Configs
from os.path import expanduser
from ticket_man.loggers import logger


async def db():
    engine = create_engine(
        # In-memory sqlite database cannot be accessed from different
        # threads, use file.
        f'sqlite://{expanduser(Configs.cfg.db.path)}', strategy=ASYNCIO_STRATEGY)
    conn = await engine.connect()  # Insert some users
