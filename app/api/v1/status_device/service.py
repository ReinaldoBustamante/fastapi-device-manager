from fastapi import HTTPException
from .repository import StatusDeviceRepository
from .schemas import CreateStatusDeviceDTO
from models import StatusDevice

class StatusDeviceService:
    def __init__(self, status_device_repository: StatusDeviceRepository):
        self.status_device_repository = status_device_repository
    
    def get_all_status_device(self):
        return self.status_device_repository.get_all_status_device()
    
    def create_status_device(self, status_device_dto: CreateStatusDeviceDTO):
        status_device_exist = self.status_device_repository.get_status_device_by_name(status_device_dto.name)
        if status_device_exist:
            raise HTTPException(status_code=409, detail="Status device already exists")
        
        status_device = StatusDevice(**status_device_dto.model_dump())
        return self.status_device_repository.create_status_device(status_device)
    
    def delete_status_device(self, status_device_id: int):
        status_device = self.status_device_repository.get_status_device_by_id(status_device_id)
        if status_device is None:
            raise HTTPException(status_code=404, detail="Status device not found")

        return self.status_device_repository.delete_status_device(status_device)