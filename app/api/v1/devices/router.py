from api.v1.devices.schemas import DeviceResumeListResponse
from api.v1.users.repository import UserRepository
from api.v1.devices.schemas import AssignDeviceDTO
from api.v1.action_logs.repository import ActionLogRepository
from .schemas import CreateDeviceDTO, DeviceResponse, UpdateStatusDeviceDTO
from .service import DeviceService
from .repository import DeviceRepository
from core.db import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from api.v1.type_device.repository import TypeDeviceRepository
from api.v1.status_device.repository import StatusDeviceRepository
from core.security import require_admin

def device_service(db: Session = Depends(get_db)):
    device_repository = DeviceRepository(db)
    status_device_repository = StatusDeviceRepository(db)
    type_device_repository = TypeDeviceRepository(db)
    action_log_repository = ActionLogRepository(db)
    user_repository = UserRepository(db)
    return DeviceService(device_repository, status_device_repository, type_device_repository, action_log_repository, user_repository)

router = APIRouter()

@router.get('/')
def get_all_device(limit: int = 10, offset: int = 0, device_service: DeviceService = Depends(device_service)):
    return device_service.get_all_device(limit, offset)

@router.get('/resume', response_model=DeviceResumeListResponse)
def get_device_resume(limit: int = 10, offset: int = 0, device_service: DeviceService = Depends(device_service)):
    return device_service.get_device_resume(limit, offset)

@router.post('/', response_model=DeviceResponse)
def create_device(create_device_dto: CreateDeviceDTO, device_service: DeviceService = Depends(device_service), current_user = Depends(require_admin)):
    return device_service.create_device(create_device_dto, current_user)

@router.put('/{device_id}/status', response_model=DeviceResponse)
def update_status_device(
    device_id: int, 
    updates_status_device_dto: UpdateStatusDeviceDTO, 
    device_service: DeviceService = Depends(device_service),  
    current_user = Depends(require_admin)
):
    return device_service.update_status_device(device_id, updates_status_device_dto, current_user)

@router.put('/{device_id}/assign')
def assign_device(
    device_id: int,
    assign_device_dto: AssignDeviceDTO,
    device_service: DeviceService = Depends(device_service),
    current_user = Depends(require_admin)
):
    return device_service.assign_device(device_id, assign_device_dto, current_user)

