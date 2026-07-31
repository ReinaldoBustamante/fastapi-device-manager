

class DashboardService:
    def __init__(self, dashboard_repository):
        self.dashboard_repository = dashboard_repository

    def get_stats(self):
        return self.dashboard_repository.get_stats()

    def get_devices(self, status_id: int | None, search: str | None, limit: int, offset: int):
        result, total = self.dashboard_repository.get_devices(status_id, search, limit, offset)
        return {
            "devices": result,
            "pagination": {
                "limit": limit,
                "offset": offset,
                "total": total
            }
        }