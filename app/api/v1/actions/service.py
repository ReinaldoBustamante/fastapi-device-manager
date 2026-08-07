
from fastapi import HTTPException
from app.api.v1.actions.repository import ActionRepository


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
