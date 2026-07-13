from pydantic import BaseModel, ConfigDict

class CreateStatusDeviceDTO(BaseModel):
    name: str


class PublicStatusDevice(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)