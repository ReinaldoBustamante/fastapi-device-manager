from sqlalchemy.orm import Session
from sqlalchemy import select
from models import TypeDevice

class TypeDeviceRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_type_device(self):
        stmt = select(TypeDevice)
        return self.db.scalars(stmt).all()

    def get_type_device_by_id(self, id: int):
        stmt = select(TypeDevice).where(TypeDevice.id == id)
        return self.db.scalars(stmt).first()

    def get_type_device_by_name(self, name: str):
        stmt = select(TypeDevice).where(TypeDevice.name == name)
        return self.db.scalars(stmt).first()
    
    def create_type_device(self, type_device: TypeDevice):
        self.db.add(type_device)
        self.db.flush()
        return type_device

    def delete_type_device(self, type_device: TypeDevice):
        self.db.delete(type_device)
        self.db.flush()
        return type_device
    