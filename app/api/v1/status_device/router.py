from typing import List
from .service import StatusDeviceService
from .repository import StatusDeviceRepository
from .schemas import StatusDeviceResponse
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.core.db import get_db

router = APIRouter()

def status_device_service(db: Session = Depends(get_db)):
    status_device_repository = StatusDeviceRepository(db)
    return StatusDeviceService(status_device_repository)

@router.get('/', response_model=List[StatusDeviceResponse])
def get_all_status_device(
    status_device_service: StatusDeviceService = Depends(status_device_service)
):
    return status_device_service.get_all_status_device()

@router.get('/{status_device_id}', response_model=StatusDeviceResponse)
def get_status_device_by_id(
    status_device_id: int, 
    status_device_service: StatusDeviceService = Depends(status_device_service)
):
    return status_device_service.get_status_device_by_id(status_device_id)