from core.security import require_admin
from typing import List
from .repository import RoleRepository
from .service import RoleServices
from .schemes import CreateRoleDTO, RolePublicResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.db import get_db

router = APIRouter()
def role_services(db: Session = Depends(get_db)):
    role_repository = RoleRepository(db)
    return RoleServices(role_repository)

@router.get('/', response_model=List[RolePublicResponse])
def get_all_roles(
    role_service: RoleServices = Depends(role_services)
):
    return role_service.get_all()

@router.post('/', response_model=RolePublicResponse)
def create_role(
    roleDTO: CreateRoleDTO, 
    role_service: RoleServices = Depends(role_services),
    _: dict = Depends(require_admin)
):
    return role_service.create(roleDTO)

@router.delete('/{role_id}', response_model=RolePublicResponse)
def delete_role(
    role_id: int,
    role_service: RoleServices = Depends(role_services),
    _: dict = Depends(require_admin)
):
    return role_service.delete(role_id)