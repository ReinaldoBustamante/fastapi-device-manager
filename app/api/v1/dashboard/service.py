

class DashboardService:
    def __init__(self, dashboard_repository):
        self.dashboard_repository = dashboard_repository

    def get_stats(self):
        return self.dashboard_repository.get_stats()

