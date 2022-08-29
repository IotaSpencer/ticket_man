__all__ = ['todo', 'Base']
from sqlalchemy.orm import declarative_base
from . import todo
# declarative base class
Base = declarative_base()
