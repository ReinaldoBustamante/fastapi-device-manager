from app.core.db import Base
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .action_logs import ActionLogs

class Action(Base):
    __tablename__ = 'action'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    
    action_logs: Mapped[List["ActionLogs"]] = relationship(back_populates='action')
    