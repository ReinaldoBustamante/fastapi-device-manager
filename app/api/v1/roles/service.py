from fastapi import HTTPException
from .repository import RoleRepository

class RoleServices:
    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository
    
    def get_all(self):
        return self.role_repository.get_all()
    
    def get_by_id(self, role_id: int):
        role = self.role_repository.get_by_id(role_id)
        if role is None:
            raise HTTPException(status_code=404, detail="Role not found")
        return role
    
