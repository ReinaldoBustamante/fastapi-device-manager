from app.utils.password import hash_password
from app.api.v1.roles.repository import RoleRepository
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException
from app.utils.password import verify_password
from app.core.security import create_token
from .repository import AuthRepository
from .schemas import CreateUserDTO
from app.models import User

class AuthService:
    def __init__(self, auth_repository: AuthRepository, role_repository: RoleRepository):
        self.auth_repository = auth_repository
        self.role_repository = role_repository

    def login(self, form_data: OAuth2PasswordRequestForm = Depends()):
        user = self.auth_repository.get_by_username(form_data.username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if not verify_password(form_data.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        token = create_token({"sub": str(user.id), "email": user.email, "role_id": user.role_id})

        return {
            "access_token": token
        }
    
    def register(self, create_user_dto: CreateUserDTO, current_user: User):
        current_role = self.role_repository.get_by_id(current_user.get('role_id'))
        if current_role.name != 'ADMIN':
            raise HTTPException(status_code=403, detail="You don't have permission to create this role")
        
        user_exist = self.auth_repository.get_by_username(create_user_dto.email)
        if user_exist:
            raise HTTPException(status_code=409, detail="User already exists")

        role = self.role_repository.get_by_id(create_user_dto.role_id)
        if role is None:
            raise HTTPException(status_code=404, detail="Role not found")
        
        user = User(**create_user_dto.model_dump())
        user.password = hash_password(user.password)
        
        return self.auth_repository.create_user(user)
        