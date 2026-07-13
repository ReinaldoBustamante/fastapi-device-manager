

from api.v1.users.repository import UserRepository
from api.v1.action_logs.repository import ActionLogRepository
from models import Device, ActionLogs
from fastapi import HTTPException
from .schemas import CreateDeviceDTO, UpdateStatusDeviceDTO, AssignDeviceDTO
from .repository import DeviceRepository
from api.v1.type_device.repository import TypeDeviceRepository
from api.v1.status_device.repository import StatusDeviceRepository
from core.enums import ActionType

class DeviceService:
    def __init__(
        self, 
        device_repository: DeviceRepository, 
        status_device_repository: StatusDeviceRepository,
        type_device_repository: TypeDeviceRepository,
        action_log_repository: ActionLogRepository,
        user_repository: UserRepository
    ):
        self.device_repository = device_repository
        self.status_device_repository = status_device_repository
        self.type_device_repository = type_device_repository
        self.action_log_repository = action_log_repository
        self.user_repository = user_repository
    
    def get_all_device(self, limit: int, offset: int):
        return self.device_repository.get_all_device(limit, offset)
    
    def create_device(self, create_device_dto: CreateDeviceDTO, current_user):
        device_exist = self.device_repository.get_device_by_serial_number(create_device_dto.serial_number)
        if device_exist:
            raise HTTPException(status_code=409, detail="Device already exists")
        
        status_device = self.status_device_repository.get_status_device_by_id(create_device_dto.status_id)
        if not status_device:
            raise HTTPException(status_code=404, detail="Status device not found")
        
        type_device = self.type_device_repository.get_type_device_by_id(create_device_dto.type_id)
        if not type_device:
            raise HTTPException(status_code=404, detail="Type device not found")
        
        device = Device(**create_device_dto.model_dump())
        self.device_repository.create_device(device)
        
        action = ActionLogs(
            action_id= ActionType.CREATE_DEVICE,
            user_id=current_user.get('id'),
            device_id=device.id,    
        )

        self.action_log_repository.add_action_log(action)
        return device

    def update_status_device(self, device_id: int, update_status_device_dto: UpdateStatusDeviceDTO, current_user):
        updates = {"status_id": update_status_device_dto.status_id}
        device = self.device_repository.get_device_by_id(device_id)
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        
        status_device = self.status_device_repository.get_status_device_by_id(update_status_device_dto.status_id)
        if not status_device:
            raise HTTPException(status_code=404, detail="Status device not found")
        
        self.device_repository.update_device(device, updates)

        action = ActionLogs(
            action_id= ActionType.UPDATE_DEVICE,
            user_id=current_user.get('id'),
            device_id=device.id,    
        )
        self.action_log_repository.add_action_log(action)
        
        return device
    
    def assign_device(self, device_id: int, assign_device_dto: AssignDeviceDTO, current_user):
        device = self.device_repository.get_device_by_id(device_id)
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        
        user = self.user_repository.get_user_by_id(assign_device_dto.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        self.device_repository.update_device(device, {"user_id": assign_device_dto.user_id})
        
        action = ActionLogs(
            action_id= ActionType.ASSIGN_DEVICE,
            user_id=current_user.get('id'),
            device_id=device.id,    
        )
        self.action_log_repository.add_action_log(action)
        
        return device

   
