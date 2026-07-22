from .schemas import CreateTypeDeviceDTO
from app.api.v1.type_device.repository import TypeDeviceRepository
from app.models import TypeDevice
from fastapi import HTTPException, status


class TypeDeviceService:
    def __init__(self, type_device_repository: TypeDeviceRepository):
        self.type_device_repository = type_device_repository
    
    def get_all_type_device(self):
        return self.type_device_repository.get_all_type_device()
    
    def get_type_device_by_name(self, name: str):
        type_device = self.type_device_repository.get_type_device_by_name(name)
        if type_device is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Type device not found")
        return type_device
    
    def create_type_device(self, type_device_dto: CreateTypeDeviceDTO):
        type_device_exist = self.type_device_repository.get_type_device_by_name(type_device_dto.name)
        if type_device_exist:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Type device already exist")
        type_device = TypeDevice(**type_device_dto.model_dump())
        return self.type_device_repository.create_type_device(type_device)
    
    def delete_type_device(self, type_device_id: int):
        type_device = self.type_device_repository.get_type_device_by_id(type_device_id)
        if type_device is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Type device not found")
        return self.type_device_repository.delete_type_device(type_device)