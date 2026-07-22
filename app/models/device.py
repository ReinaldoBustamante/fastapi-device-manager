from typing import Optional
from app.core.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, Date, ForeignKey
from datetime import datetime, date, timezone
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .status_device import StatusDevice
    from .type_device import TypeDevice
    from .action_logs import ActionLogs
    from .user import User

class Device(Base):
    __tablename__ = 'device'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    serial_number: Mapped[str]= mapped_column(String(255), nullable=False, unique=True)
    brand: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    buy_date: Mapped[date] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(tz=timezone.utc))
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, default=None, onupdate=lambda: datetime.now(tz=timezone.utc))
    status_id: Mapped[int] = mapped_column(Integer, ForeignKey("status_device.id"), nullable=False) 
    type_id: Mapped[int] = mapped_column(Integer, ForeignKey("type_device.id"), nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("user.id"), nullable=True)

    status: Mapped["StatusDevice"] = relationship(back_populates="devices")
    type: Mapped["TypeDevice"] = relationship(back_populates="devices")
    action_logs: Mapped[List["ActionLogs"]] = relationship(back_populates="device")

    user: Mapped[Optional["User"]] = relationship(back_populates="devices")
