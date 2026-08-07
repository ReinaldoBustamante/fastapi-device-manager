
from app.api.v1.dashboard.schemas import DashboardResponse
from app.core.db import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter
from app.api.v1.dashboard.repository import DashboardRepository
from app.api.v1.dashboard.service import DashboardService

router = APIRouter()
def dashboard_service(db: Session = Depends(get_db)):
    dashboard_repository = DashboardRepository(db)
    return DashboardService(dashboard_repository)

@router.get('/stats', response_model=DashboardResponse)
def get_stats(dashboard_service: DashboardService = Depends(dashboard_service)):
    return dashboard_service.get_stats()
