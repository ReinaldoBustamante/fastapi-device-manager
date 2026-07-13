from api.v1.users.service import UserService
from api.v1.users.repository import UserRepository
from core.db import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from .schemas import UserResponse, PaginatedUserResponse

router = APIRouter()

def user_service(db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    return UserService(user_repository)

@router.get('/', response_model=PaginatedUserResponse)
def get_all(
    offset: int = 0, 
    limit: int = 10, 
    user_service: UserService = Depends(user_service)
):
    return user_service.get_all_users(limit, offset)

@router.get('/{user_id}', response_model=UserResponse)
def get_user(
    user_id: int, 
    user_service: UserService = Depends(user_service)
):
    return user_service.get_user_by_id(user_id)

@router.get('/{user_id}/devices')
def get_user_devices(
    user_id: int,
    user_service: UserService = Depends(user_service)
):
    return user_service.get_user_devices(user_id)
