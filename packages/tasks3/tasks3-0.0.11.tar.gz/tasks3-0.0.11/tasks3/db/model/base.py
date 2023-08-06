"""Base model for the Database."""
import uuid

from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base(object):
    """Declarative base class for tasks3's database."""

    @declared_attr
    def __tablename__(cls) -> str:
        """Automatically set the correct table name for the inheriting classes"""
        return str.lower(cls.__name__)

    id = Column(
        String(length=6), primary_key=True, default=lambda: str(uuid.uuid4())[:6]
    )
