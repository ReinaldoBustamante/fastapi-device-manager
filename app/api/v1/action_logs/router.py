from app.core.security import require_admin
from app.api.v1.action_logs.service import ActionLogService
from app.api.v1.action_logs.repository import ActionLogRepository
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.core.db import get_db

router = APIRouter()

def action_log_service(db: Session = Depends(get_db)):
    action_log_repository = ActionLogRepository(db)
    return ActionLogService(action_log_repository)


@router.get('/')
def get_action_logs(
    offset: int = 0, 
    limit: int = 10, 
    action_log_service: ActionLogService = Depends(action_log_service),
    _: dict = Depends(require_admin)
):
    return action_log_service.get_action_logs(offset, limit)