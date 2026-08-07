
from app.models import Device
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import Session

class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_stats(self):
        total = self.db.scalar(select(func.count()).select_from(Device))
        available = self.db.scalar(select(func.count()).select_from(Device).where(Device.status_id == 1))
        assigned = self.db.scalar(select(func.count()).select_from(Device).where(Device.status_id == 2))
        in_repair = self.db.scalar(select(func.count()).select_from(Device).where(Device.status_id == 3))
        losts = self.db.scalar(select(func.count()).select_from(Device).where(Device.status_id == 4))
        retired = self.db.scalar(select(func.count()).select_from(Device).where(Device.status_id == 5))
        
        return {
            "total": total,
            "available": available,
            "assigned": assigned,
            "in_repair": in_repair,
            "losts": losts,
            "retired": retired
        }
    
