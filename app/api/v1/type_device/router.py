from core.security import require_admin
from typing import List
from core.db import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from .schemas import CreateTypeDeviceDTO, PublicTypeDevice
from .service import TypeDeviceService
from .repository import TypeDeviceRepository


router = APIRouter()

def type_device_service(db: Session = Depends(get_db)):
    type_device_repository = TypeDeviceRepository(db)
    return TypeDeviceService(type_device_repository)


@router.get('/', response_model=List[PublicTypeDevice])
def get_all_type_device(type_device_service: TypeDeviceService = Depends(type_device_service)):
    return type_device_service.get_all_type_device()

@router.post('/', response_model=PublicTypeDevice)
def create_type_device(
    type_device_dto: CreateTypeDeviceDTO, 
    type_device_service: TypeDeviceService = Depends(type_device_service),
    _: dict = Depends(require_admin)
):
    return type_device_service.create_type_device(type_device_dto)

@router.delete('/{type_device_id}', response_model=PublicTypeDevice)
def delete_type_device(
    type_device_id: int, 
    type_device_service: TypeDeviceService = Depends(type_device_service),
    _: dict = Depends(require_admin)
):
    return type_device_service.delete_type_device(type_device_id)