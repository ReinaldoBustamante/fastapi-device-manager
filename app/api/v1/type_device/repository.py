from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import TypeDevice

class TypeDeviceRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_type_device(self):
        stmt = select(TypeDevice)
        return self.db.scalars(stmt).all()

    def get_type_device_by_id(self, id: int):
        stmt = select(TypeDevice).where(TypeDevice.id == id)
        return self.db.scalars(stmt).first()