from sqlalchemy.orm import selectinload
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models import Device

class DeviceRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_device(self, limit: int, offset: int):
        stmt = select(Device).limit(limit).offset(offset)
        devices = self.db.scalars(stmt).all()

        total = self.db.scalar(
            select(func.count()).select_from(Device)
        )

        return {
            "devices": devices,
            "pagination": {
                "total": total,
                "offset": offset,
                "limit": limit
            }
        }

    def get_device_by_id(self, device_id: int):
        stmt = select(Device).where(Device.id == device_id)
        result = self.db.scalars(stmt).first()
        return result

    def get_device_resume(self, limit:int, offset:int):
        stmt = select(Device).options(selectinload(Device.user), selectinload(Device.type), selectinload(Device.status)).limit(limit).offset(offset)
        devices = self.db.scalars(stmt).all()
        
        total = self.db.scalar(
            select(func.count()).select_from(Device)
        )

        available = self.db.scalar(
            select(func.count()).select_from(Device).where(Device.status_id == 1)
        )

        assigned = self.db.scalar(
            select(func.count()).select_from(Device).where(Device.status_id == 2)
        )

        in_repair = self.db.scalar(
            select(func.count()).select_from(Device).where(Device.status_id == 3)
        )

        losts = self.db.scalar(
            select(func.count()).select_from(Device).where(Device.status_id == 4)
        )

        retired = self.db.scalar(
            select(func.count()).select_from(Device).where(Device.status_id == 5)
        )
        
        return {
            "devices": devices,
            "stats": {
                "total": total,
                "available": available,
                "assigned": assigned,
                "in_repair": in_repair,
                "losts": losts,
                "retired": retired
            },
            "pagination": {
                "total": total,
                "offset": offset,
                "limit": limit
            }
        }

    def create_device(self, device: Device):
        self.db.add(device)
        self.db.flush()
        return device
    
    def update_device(self, device: Device, update_device: dict):
        for key, value in update_device.items():
            setattr(device, key, value)
        self.db.flush()
        return device
    
    def get_device_by_serial_number(self, serial_number: str):
        stmt = select(Device).where(Device.serial_number == serial_number)
        result = self.db.scalars(stmt).first()
        return result