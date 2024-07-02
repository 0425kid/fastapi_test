from pydantic import BaseModel

# Pydantic model for caregiver registration
class CaregiverCreate(BaseModel):
    name: str
    age: int
    gender: str
    phone: str
    address: str
    experience: str
    desired_hourly_rate: int

# Pydantic model for caregiver response
class CaregiverResponse(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    phone: str
    address: str
    experience: str
    desired_hourly_rate: int

    class Config:
        orm_mode = True
