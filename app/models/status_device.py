from core.db import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .device import Device



class StatusDevice(Base):
    __tablename__ = "status_device"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    
    devices: Mapped[List["Device"]] = relationship(back_populates="status")

