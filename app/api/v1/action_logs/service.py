from .repository import ActionLogRepository
from .schemas import ActionLogDTO
from models import ActionLogs
class ActionLogService:
    def __init__(self, action_log_repository: ActionLogRepository):
        self.action_log_repository = action_log_repository

    def add_action_log(self, action_log: ActionLogDTO):
        action_log = ActionLogs(**action_log.model_dump())
        return self.action_log_repository.add_action_log(action_log)

    def get_action_logs(self, offset: int, limit: int):
        return self.action_log_repository.get_action_logs(offset, limit)