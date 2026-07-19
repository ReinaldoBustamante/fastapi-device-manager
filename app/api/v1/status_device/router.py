from core.security import require_admin
from typing import List
from .service import StatusDeviceService
from .repository import StatusDeviceRepository
from .schemas import PublicStatusDevice, CreateStatusDeviceDTO
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from core.db import get_db

router = APIRouter()

def status_device_service(db: Session = Depends(get_db)):
    status_device_repository = StatusDeviceRepository(db)
    return StatusDeviceService(status_device_repository)

@router.get('/', response_model=List[PublicStatusDevice])
def get_all_status_device(status_device_service: StatusDeviceService = Depends(status_device_service)):
    return status_device_service.get_all_status_device()

@router.post('/', response_model=PublicStatusDevice)
def create_status_device(
    status_device_dto: CreateStatusDeviceDTO, 
    status_device_service: StatusDeviceService = Depends(status_device_service),
    _: dict = Depends(require_admin)
):
    return status_device_service.create_status_device(status_device_dto)

@router.delete('/{status_device_id}', response_model=PublicStatusDevice)
def delete_status_device(
    status_device_id: int, 
    status_device_service: StatusDeviceService = Depends(status_device_service),
    _: dict = Depends(require_admin)
):
    return status_device_service.delete_status_device(status_device_id)