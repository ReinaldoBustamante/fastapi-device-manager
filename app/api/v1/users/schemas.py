from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class UpdateUserDTO(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role_id: Optional[int] = None


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    is_active: bool
    role_id: int

    model_config = ConfigDict(from_attributes=True)

class PaginationResponse(BaseModel):
    total: int
    offset: int
    limit: int

class PaginatedUserResponse(BaseModel):
    users: List[UserResponse]
    pagination: PaginationResponse