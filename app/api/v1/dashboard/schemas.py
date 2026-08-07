from pydantic import BaseModel

class DashboardResponse(BaseModel):
    total: int
    available: int
    assigned: int
    in_repair: int
    losts: int
    retired: int