from app.core.db import Base
from sqlalchemy import Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .device import Device
    from .user import User
    from .action import Action

class ActionLogs(Base):
    __tablename__ = "action_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[int] = mapped_column(Integer, ForeignKey("device.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    action_id: Mapped[int] = mapped_column(Integer, ForeignKey("action.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(tz=timezone.utc))
    
    device: Mapped["Device"] = relationship(back_populates="action_logs")
    user: Mapped["User"] = relationship(back_populates="action_logs")
    action: Mapped["Action"] = relationship(back_populates="action_logs")

  