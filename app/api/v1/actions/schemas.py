from pydantic import BaseModel, ConfigDict

class CreateActionDTO(BaseModel):
    name: str

class ActionResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
