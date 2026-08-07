from typing import List
from .repository import RoleRepository
from .service import RoleServices
from .schemas import RolePublicResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db

router = APIRouter()
def role_services(db: Session = Depends(get_db)):
    role_repository = RoleRepository(db)
    return RoleServices(role_repository)

@router.get('/', response_model=List[RolePublicResponse])
def get_all_roles(
    role_service: RoleServices = Depends(role_services)
):
    return role_service.get_all()

@router.get('/{role_id}', response_model=RolePublicResponse)
def get_role_by_id(role_id: int, role_services = Depends(role_services)):
    return role_services.get_by_id(role_id)