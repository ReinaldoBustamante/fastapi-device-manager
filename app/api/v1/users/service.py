from app.models import User
from app.utils.password import hash_password
from app.api.v1.users.schemas import CreateUserDTO
from fastapi import HTTPException
from app.api.v1.users.repository import UserRepository
from app.api.v1.devices.repository import DeviceRepository

class UserService:
    def __init__(self, user_repository: UserRepository, device_repository: DeviceRepository):
        self.user_repository = user_repository
        self.device_repository = device_repository

    def get_all_users(self, limit: int, offset: int, search: str):
        users, total = self.user_repository.get_all_users(limit, offset, search)
        return {
            "users": users,
            "pagination": {
                "total": total,
                "offset": offset,
                "limit": limit
            }
        }
    
    def get_user_by_id(self, user_id: int):
        user = self.user_repository.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    def get_user_devices(self, user_id: int):
        user = self.get_user_by_id(user_id)
        return user.devices

    def create_user(self, create_user_dto: CreateUserDTO):
        user_exist = self.user_repository.get_user_by_email(create_user_dto.email)
        if user_exist:
            raise HTTPException(status_code=409, detail="User already exists")
        
        password_hashed = hash_password(create_user_dto.password)

        user = User(
            first_name=create_user_dto.first_name,
            last_name=create_user_dto.last_name,
            email=create_user_dto.email,
            password=password_hashed,
            role_id=2
        )
        self.user_repository.create_user(user)
        return user

    def deactivate_user(self, user_id: int):
        user_exist = self.user_repository.get_user_by_id(user_id)
        if user_exist is None:
            raise HTTPException(status_code=404, detail="User not found")
        if not user_exist.is_active:
            raise HTTPException(status_code=409, detail="User is already inactive")
        
        self.user_repository.patch_user(user_exist, {"is_active": False})
        for device in user_exist.devices:
            self.device_repository.update_device(device, {"user_id": None})
        
        return {
            "message": "User deactivated successfully"
        }
