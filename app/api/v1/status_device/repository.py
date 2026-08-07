from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import StatusDevice

class StatusDeviceRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_status_device(self):
        stmt = select(StatusDevice)
        result = self.db.execute(stmt)
        return result.scalars().all()

    def get_status_device_by_id(self, status_device_id: int):
        stmt = select(StatusDevice).where(StatusDevice.id == status_device_id)
        result = self.db.scalars(stmt).first()
        return result
