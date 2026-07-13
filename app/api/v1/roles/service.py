

from fastapi import HTTPException
from .repository import RoleRepository
from .schemes import CreateRoleDTO
from models import Role

class RoleServices:
    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository
    
    def get_all(self):
        return self.role_repository.get_all()
    
    def create(self, roleDTO: CreateRoleDTO):
        role_exist = self.role_repository.get_by_name(roleDTO.name)
        if role_exist:
            raise HTTPException(status_code=409, detail="Role already exists")

        role = Role(**roleDTO.model_dump())
        return self.role_repository.create(role)
    
    def delete(self, role_id: int):
        role = self.role_repository.get_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        return self.role_repository.delete(role)
