
from fastapi import HTTPException
from api.v1.actions.schemas import CreateActionDTO
from api.v1.actions.repository import ActionRepository
from models import Action


class ActionService:
    def __init__(self, action_repository: ActionRepository):
        self.action_repository = action_repository
    
    def get_all_actions(self):
        return self.action_repository.get_all_actions()
    
    def get_action_by_id(self, action_id: int):
        action = self.action_repository.get_action_by_id(action_id)
        if action is None:
            raise HTTPException(status_code=404, detail="Action not found")
        return action

    def create_action(self, actionDTO: CreateActionDTO):
        action_exist = self.action_repository.get_action_by_name(actionDTO.name)
        if action_exist:
            raise HTTPException(status_code=409, detail=f"Action {actionDTO.name} already exists")
        action = Action(**actionDTO.model_dump())
        return self.action_repository.create_action(action)
    
    def delete_action(self, action_id: int ):
        action = self.get_action_by_id(action_id)
        if len(action.action_logs) > 0:
            raise HTTPException(status_code=400, detail="Action has logs")

        return self.action_repository.delete_action(action)