from app.api.v1.type_device.repository import TypeDeviceRepository
from fastapi import HTTPException, status


class TypeDeviceService:
    def __init__(self, type_device_repository: TypeDeviceRepository):
        self.type_device_repository = type_device_repository
    
    def get_all_type_device(self):
        return self.type_device_repository.get_all_type_device()
    
    def get_type_device_by_id(self, type_device_id: int):
        type_device = self.type_device_repository.get_type_device_by_id(type_device_id)
        if type_device is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Type device not found")
        return type_device