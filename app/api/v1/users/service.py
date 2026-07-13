from fastapi import HTTPException
from api.v1.users.repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_all_users(self, limit: int, offset: int):
        return self.user_repository.get_all_users(limit, offset)
    
    def get_user_by_id(self, user_id: int):
        user = self.user_repository.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    def get_user_devices(self, user_id: int):
        user = self.get_user_by_id(user_id)
        return user.devices

  