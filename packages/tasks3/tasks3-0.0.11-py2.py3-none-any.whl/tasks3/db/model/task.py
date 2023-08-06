"""Task database model"""

from tasks3.db import model

from collections import OrderedDict as odict
from sqlalchemy import Column, Unicode, Integer, UnicodeText, CheckConstraint, JSON


class Task(model.Base):
    """Task database model

    SQLAlchemy uses this class to define and interact with the
    Task Table in the database.
    """

    title = Column(Unicode, nullable=False)
    urgency = Column(Integer, nullable=False)
    importance = Column(Integer, nullable=False)
    tags = Column(JSON, nullable=False)
    folder = Column(Unicode)
    description = Column(UnicodeText)

    __table_args__ = (
        CheckConstraint(0 <= urgency, "Urgency interval check"),
        CheckConstraint(urgency <= 4, "Urgency interval check"),
        CheckConstraint(0 <= importance, "Importance interval check"),
        CheckConstraint(importance <= 4, "Importance interval check"),
    )

    def _to_dict(self) -> odict:
        return odict(
            id=self.id,
            title=self.title,
            urgency=self.urgency,
            importance=self.importance,
            tags=self.tags,
            folder=self.folder,
            description=self.description,
        )

    def __repr__(self) -> str:
        return f"<Task{self._to_dict().__repr__()}>"
