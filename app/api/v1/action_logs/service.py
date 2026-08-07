from .repository import ActionLogRepository

class ActionLogService:
    def __init__(self, action_log_repository: ActionLogRepository):
        self.action_log_repository = action_log_repository

    def get_action_logs(self, offset: int, limit: int):
        logs, total = self.action_log_repository.get_action_logs(offset, limit)
        return {
            "data": logs,
            "pagination": {
                "total": total,
                "offset": offset,
                "limit": limit
            }
        }