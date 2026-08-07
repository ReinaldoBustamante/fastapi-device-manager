from typing import List
from app.core.db import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from .schemas import TypeDeviceResponse
from .service import TypeDeviceService
from .repository import TypeDeviceRepository


router = APIRouter()

def type_device_service(db: Session = Depends(get_db)):
    type_device_repository = TypeDeviceRepository(db)
    return TypeDeviceService(type_device_repository)


@router.get('/', response_model=List[TypeDeviceResponse])
def get_all_type_device(
    type_device_service: TypeDeviceService = Depends(type_device_service)
):
    return type_device_service.get_all_type_device()

@router.get('/{type_device_id}', response_model=TypeDeviceResponse)
def get_type_device_by_id(
    type_device_id: int,
    type_device_service: TypeDeviceService = Depends(type_device_service)
):
    return type_device_service.get_type_device_by_id(type_device_id)