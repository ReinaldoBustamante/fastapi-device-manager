

from app.api.v1.devices.schemas import CreateDeviceDTO
from app.api.v1.users.repository import UserRepository
from app.api.v1.action_logs.repository import ActionLogRepository
from app.models import ActionLogs
from fastapi import HTTPException
from .schemas import UpdateStatusDeviceDTO, AssignDeviceDTO
from .repository import DeviceRepository
from app.api.v1.type_device.repository import TypeDeviceRepository
from app.api.v1.status_device.repository import StatusDeviceRepository
from app.core.enums import ActionType
from app.models import Device

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
    
    def get_all_devices(self, status_id: int | None, search: str | None, limit: int, offset: int):
        result, total = self.device_repository.get_all_devices(status_id, search, limit, offset)
        return {
            "devices": result,
            "pagination": {
                "limit": limit,
                "offset": offset,
                "total": total
            }
        }

    def get_device_by_id(self, device_id):
        result = self.device_repository.get_device_by_id(device_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Device not found")
        return result

    def create_device(self, create_device_dto: CreateDeviceDTO, current_user):
        serial_number = self.device_repository.get_device_by_serial_number(create_device_dto.serial_number)
        if serial_number:
            raise HTTPException(status_code=409, detail="Serial number already exists")
        status_id = self.status_device_repository.get_status_device_by_id(create_device_dto.status_id)
        if not status_id:
            raise HTTPException(status_code=404, detail="Status device not found")
        type_id = self.type_device_repository.get_type_device_by_id(create_device_dto.type_id)
        if not type_id:
            raise HTTPException(status_code=404, detail="Type device not found")

        device = Device(**create_device_dto.model_dump())
        result = self.device_repository.create_device(device)
        action = ActionLogs(
            action_id= ActionType.CREATE_DEVICE,
            user_id=current_user.get('id'),
            device_id=result.id,
        )
        self.action_log_repository.add_action_log(action)
        return result
        

    def update_status_device(self, device_id: int, update_status_device_dto: UpdateStatusDeviceDTO, current_user):
        updates = update_status_device_dto.model_dump(exclude_unset=True)
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
            device_id=device_id,    
        )

        self.action_log_repository.add_action_log(action)
        
        return "Device status updated successfully"
    
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
            device_id=device_id,    
        )
        self.action_log_repository.add_action_log(action)
        
        return "Device assigned successfully"
