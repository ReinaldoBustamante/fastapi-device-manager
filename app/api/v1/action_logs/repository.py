from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models import ActionLogs

class ActionLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_action_log(self, action_log: ActionLogs):
        self.db.add(action_log)
        self.db.flush()
        return action_log
    
    def get_action_logs(self, offset: int, limit: int):
        query= select(ActionLogs).limit(limit).offset(offset)
        result = self.db.scalars(query).all()

        total = self.db.scalar(
            select(func.count()).select_from(ActionLogs)
        )

        return result, total
