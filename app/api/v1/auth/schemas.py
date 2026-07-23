from pydantic import ConfigDict
from pydantic import BaseModel
from datetime import date

class CreateUserDTO(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    role_id: int
    
class LoginResponse(BaseModel):
    access_token: str

class RegisterResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    role_id: int

    model_config = ConfigDict(from_attributes=True)