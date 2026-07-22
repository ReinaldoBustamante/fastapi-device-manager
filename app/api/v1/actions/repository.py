from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Action

class ActionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_actions(self):
        stmt = select(Action)
        return self.db.scalars(stmt).all()
    
    def get_action_by_id(self, action_id: int):
        stmt = select(Action).where(Action.id == action_id)
        return self.db.scalars(stmt).first()

    def get_action_by_name(self, action_name: str):
        stmt = select(Action).where(Action.name == action_name)
        return self.db.scalars(stmt).first()

    def create_action(self, action: Action):
        self.db.add(action)
        self.db.flush()
        return action
    
    def delete_action(self, action: Action):
        self.db.delete(action)
        self.db.flush()
        return action

    
