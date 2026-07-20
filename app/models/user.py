from typing import TYPE_CHECKING, List
from sqlalchemy import Integer, String, Date, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date, timezone
from core.db import Base

if TYPE_CHECKING:
    from .role import Role
    from .action_logs import ActionLogs
    from .device import Device

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("role.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(tz=timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, onupdate=datetime.now(tz=timezone.utc))

    role: Mapped["Role"] = relationship(back_populates="users")
    action_logs: Mapped[List["ActionLogs"]] = relationship(back_populates="user")

    devices: Mapped[List["Device"]] = relationship(back_populates="user")