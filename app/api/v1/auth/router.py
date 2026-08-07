from app.api.v1.roles.repository import RoleRepository
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.db import get_db
from .schemas import LoginResponse
from .repository import AuthRepository
from .service import AuthService

router = APIRouter()

def auth_service(db: Session = Depends(get_db)):
    auth_repository = AuthRepository(db)
    role_repository = RoleRepository(db)
    return AuthService(auth_repository, role_repository)

@router.post('/login', response_model=LoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    auth_service: AuthService = Depends(auth_service)
):
    return auth_service.login(form_data)