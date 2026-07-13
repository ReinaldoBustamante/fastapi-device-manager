from pydantic import BaseModel, ConfigDict

class ActionLogDTO(BaseModel):
    id: int