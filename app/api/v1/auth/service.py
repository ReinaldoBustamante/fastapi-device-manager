from app.api.v1.roles.repository import RoleRepository
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException
from app.utils.password import verify_password
from app.core.security import create_token
from .repository import AuthRepository

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
