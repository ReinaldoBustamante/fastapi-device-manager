from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ActionLogsResponse(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    device_id: int
    action_id: int

    model_config = ConfigDict(from_attributes=True)

class PaginationResponse(BaseModel):
    total: int
    limit: int
    offset: int

class ActionLogsListResponse(BaseModel):
    data: list[ActionLogsResponse]
    pagination: PaginationResponse