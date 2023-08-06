"""Database for tasks3"""

from .model import Base, Task  # noqa: F401
from .db import init, drop, purge  # noqa: F401
