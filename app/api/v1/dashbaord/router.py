
from app.core.db import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter
from app.api.v1.dashbaord.repository import DashboardRepository
from app.api.v1.dashbaord.service import DashboardService

router = APIRouter()
def dashboard_service(db: Session = Depends(get_db)):
    dashboard_repository = DashboardRepository(db)
    return DashboardService(dashboard_repository)

@router.get('/stats')
def get_stats(dashboard_service: DashboardService = Depends(dashboard_service)):
    return dashboard_service.get_stats()

@router.get('/devices')
def get_devices(
    status_id: int | None = None, 
    search: str | None = None,
    limit: int = 10,
    offset: int = 0,
    dashboard_service: DashboardService = Depends(dashboard_service)
):
    return dashboard_service.get_devices(status_id, search, limit, offset)

