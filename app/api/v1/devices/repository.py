from sqlalchemy import select, func
from sqlalchemy.orm import Session
from models import Device

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