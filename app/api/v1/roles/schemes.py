from pydantic import BaseModel, ConfigDict


class CreateRoleDTO(BaseModel):
    name: str
    description: str

class RolePublicResponse(BaseModel):
    id: int
    name: str
    description: str
    model_config = ConfigDict(from_attributes=True)