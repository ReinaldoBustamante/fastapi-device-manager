from api.v1.actions.schemas import CreateActionDTO, ActionResponse
from api.v1.actions.service import ActionService
from api.v1.actions.repository import ActionRepository
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from core.db import get_db
from typing import List

router = APIRouter()

def action_service(db: Session = Depends(get_db)):
    action_repository = ActionRepository(db)
    return ActionService(action_repository)

@router.get('/', response_model=List[ActionResponse])
def get_all_actions(action_service: ActionService = Depends(action_service)):
    return action_service.get_all_actions()

@router.post('/', response_model=ActionResponse)
def create_action(action: CreateActionDTO, action_service: ActionService = Depends(action_service)):
    return action_service.create_action(action)

@router.delete('/{action_id}', response_model=ActionResponse)
def delete_action(action_id: int, action_service: ActionService = Depends(action_service)):
    return action_service.delete_action(action_id)