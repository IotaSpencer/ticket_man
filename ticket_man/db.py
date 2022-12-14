import asyncio
from asyncio import current_task

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ticket_man.config import Configs

dbcfg = Configs.cfg.db
db_engine = create_engine(
        f'{dbcfg.proto}://{dbcfg.user}:{dbcfg.password}@{dbcfg.host}/{dbcfg.database}?charset=utf8mb4&read_timeout=30&write_timeout=30&connect_timeout=30',
        echo=True)
session = sessionmaker(db_engine, expire_on_commit=True, future=True)
