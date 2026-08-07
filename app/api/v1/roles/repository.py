
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Role

class RoleRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self):
        stmt = select(Role)
        result = self.db.scalars(stmt).all()
        return result
    
    def get_by_id(self, role_id: int):
        stmt = select(Role).where(Role.id == role_id)
        result = self.db.scalars(stmt).first()
        return result