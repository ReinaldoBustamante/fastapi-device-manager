from typing import List
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class CreateUserDTO(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str = Field(..., min_length=8, description="Mínimo 8 caracteres")

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

class PublicUserDevices(BaseModel):
    id: int
    serial_number: str
    brand: str
    model: str
    type_id: int
    status_id: int
    model_config = ConfigDict(from_attributes=True)