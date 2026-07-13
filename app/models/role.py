from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING

from core.db import Base

if TYPE_CHECKING:
    from .user import User

class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    users: Mapped[List["User"]] = relationship(back_populates="role")