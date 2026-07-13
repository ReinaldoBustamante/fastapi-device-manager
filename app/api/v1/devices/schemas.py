from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import date, datetime

class DeviceResponse(BaseModel):
    id: int
    serial_number: str
    brand: str
    model: str
    buy_date: date
    status_id: int
    type_id: int
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class CreateDeviceDTO(BaseModel):
    serial_number: str
    brand: str
    model: str
    buy_date: date
    status_id: int
    type_id: int

class UpdateStatusDeviceDTO(BaseModel):
    status_id: int

class AssignDeviceDTO(BaseModel):
    user_id: int