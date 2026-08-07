from sqlalchemy import or_
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models import Device

class DeviceRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_devices(self, status_id: int | None, search: str | None, limit: int, offset: int):
        query = select(Device)
        if status_id:
            query = query.where(Device.status_id == status_id)
        if search:
            query = query.where(or_(
                Device.brand.ilike(f"%{search}%"),
                Device.model.ilike(f"%{search}%"),
                Device.serial_number.ilike(f"%{search}%"),
            ))
        total = self.db.scalar(select(func.count()).select_from(query.subquery()))
        query = query.limit(limit).offset(offset)
        result = self.db.scalars(query).all()
        
        return result, total

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

   
        