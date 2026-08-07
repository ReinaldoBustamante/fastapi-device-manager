from fastapi import HTTPException
from .repository import StatusDeviceRepository

class StatusDeviceService:
    def __init__(self, status_device_repository: StatusDeviceRepository):
        self.status_device_repository = status_device_repository
    
    def get_all_status_device(self):
        return self.status_device_repository.get_all_status_device()
    
    def get_status_device_by_id(self, status_device_id: int):
        status_device = self.status_device_repository.get_status_device_by_id(status_device_id)
        if status_device is None:
            raise HTTPException(status_code=404, detail="Status device not found")
        return status_device