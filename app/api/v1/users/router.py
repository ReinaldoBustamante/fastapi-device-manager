from fastapi import status
from app.api.v1.devices.repository import DeviceRepository
from app.api.v1.users.schemas import CreateUserDTO
from app.core.security import require_admin
from app.api.v1.users.schemas import PublicUserDevices, UserResponse, PaginatedUserResponse
from app.api.v1.users.service import UserService
from app.api.v1.users.repository import UserRepository
from app.core.db import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

router = APIRouter()

def user_service(db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    device_repository = DeviceRepository(db)
    return UserService(user_repository, device_repository)

@router.get('/', response_model=PaginatedUserResponse)
def get_all(
    offset: int = 0, 
    limit: int = 10, 
    search: str | None = None,
    user_service: UserService = Depends(user_service)
):
    return user_service.get_all_users(limit, offset, search)

@router.get('/{user_id}', response_model=UserResponse)
def get_user(
    user_id: int, 
    user_service: UserService = Depends(user_service)
):
    return user_service.get_user_by_id(user_id)

@router.get('/{user_id}/devices', response_model=list[PublicUserDevices])
def get_user_devices(
    user_id: int,
    user_service: UserService = Depends(user_service)
):
    return user_service.get_user_devices(user_id)

@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    create_user_dto: CreateUserDTO, 
    user_service: UserService = Depends(user_service),
    _ = Depends(require_admin)
):
    return user_service.create_user(create_user_dto)

@router.patch('/{user_id}/deactivate')
def deactivate_user(
    user_id: int,
    user_service: UserService = Depends(user_service),
    _ = Depends(require_admin)
):
    return user_service.deactivate_user(user_id)