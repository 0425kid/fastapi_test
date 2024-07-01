from pydantic import BaseModel

class CaregiverCreate(BaseModel):
    name: str
    age: int
    gender: str
    phone_number: str
    address: str
    career: str
    desired_hourly_rate: int

class CaregiverResponse(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    phone_number: str
    address: str
    career: str
    desired_hourly_rate: int

    class Config:
        orm_mode = True
