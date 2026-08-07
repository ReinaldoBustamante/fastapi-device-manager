from app.api.v1.actions.schemas import ActionResponse
from app.api.v1.actions.service import ActionService
from app.api.v1.actions.repository import ActionRepository
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.core.db import get_db
from typing import List

router = APIRouter()

def action_service(db: Session = Depends(get_db)):
    action_repository = ActionRepository(db)
    return ActionService(action_repository)

@router.get('/', response_model=List[ActionResponse])
def get_all_actions(action_service: ActionService = Depends(action_service)):
    return action_service.get_all_actions()

@router.get('/{action_id}', response_model=ActionResponse)
def get_action_by_id(action_id: int, action_service = Depends(action_service)):
    return action_service.get_action_by_id(action_id)