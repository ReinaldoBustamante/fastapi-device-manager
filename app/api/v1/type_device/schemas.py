from pydantic import BaseModel, ConfigDict


class CreateTypeDeviceDTO(BaseModel):
    name: str


class PublicTypeDevice(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)