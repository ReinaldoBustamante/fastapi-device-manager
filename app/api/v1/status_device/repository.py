from sqlalchemy import select
from sqlalchemy.orm import Session
from models import StatusDevice

class StatusDeviceRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_status_device(self):
        stmt = select(StatusDevice)
        result = self.db.execute(stmt)
        return result.scalars().all()
    
    def get_status_device_by_name(self, name: str):
        stmt = select(StatusDevice).where(StatusDevice.name == name)
        result = self.db.scalars(stmt).first()
        return result

    def get_status_device_by_id(self, status_device_id: int):
        stmt = select(StatusDevice).where(StatusDevice.id == status_device_id)
        result = self.db.scalars(stmt).first()
        return result

    def create_status_device(self, status_device: StatusDevice):
        self.db.add(status_device)
        self.db.flush()
        return status_device
    
    def delete_status_device(self, status_device: StatusDevice):
        self.db.delete(status_device)
        self.db.flush()
        return status_device