from app.core.db import Base
from sqlalchemy import Table, Column, Integer, ForeignKey

user_device = Table(
    "user_device",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("device_id", Integer, ForeignKey("device.id"), primary_key=True)
)