from pydantic import BaseModel, conint, conlist
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class CaregiverBase(BaseModel):
    name: str
    age: int
    gender: str
    phone: str
    address: str

# Pydantic model for caregiver registration
class CaregiverCreate(CaregiverBase):
    username: str
    email: str
    password: str

# Pydantic model for caregiver response
class CaregiverResponse(CaregiverBase):
    id: int
    username: str
    email: str
    points: int

    class Config:
        orm_mode = True

# 요양사 프로필
class CaregiverProfileBase(BaseModel):
    experience_ids: List[int]
    desired_hourly_rate: Optional[int] = None
    activity_start_time: Optional[datetime] = None
    activity_end_time: Optional[datetime] = None


class CaregiverProfileUpdate(CaregiverProfileBase):
    username: str
    pass

class CaregiverProfileResponse(CaregiverProfileBase):
    id: int
    caregiver_id: int
    

    class Config:
        orm_mode = True


# 보호자
class GuardianBase(BaseModel):
    name: str
    age: int
    gender: str
    phone: str
    address: str
    username: str
    email: str
    password: str

    service_urgency_index: int
    

class GuardianCreate(GuardianBase):
    relationship_index: int

    class Config:
        orm_mode = True

class GuardianResponse(GuardianBase):
    id: int
    relationship: str  # 실제 관계명을 저장할 필드
    points: int

    class Config:
        orm_mode = True

class RelationshipResponse(BaseModel):
    id: int
    relationship_type: str  # 실제 관계명을 저장할 필드

    class Config:
        orm_mode = True


class MessageCreate(BaseModel):
    sender_username: str
    receiver_username: str
    content: str


class CaregivingBase(BaseModel):
    username: str
    start_date: datetime
    end_date: datetime
    care_days: Optional[List[str]] = None
    start_time: datetime
    end_time: datetime
    extra_days: Optional[List[datetime]] = None
    address: str
    medications: Optional[List[str]] = None
    note: Optional[str] = None
    urgent_fee: int = None
    severe_fee: int = None

class CaregivingBase(BaseModel):
    username: str
    start_date: datetime
    end_date: datetime
    care_days: Optional[List[str]] = None
    start_time: datetime
    end_time: datetime
    extra_days: Optional[List[datetime]] = None
    address: str
    medications: Optional[List[str]] = None
    note: Optional[str] = None
    urgent_fee: Optional[int] = None
    severe_fee: Optional[int] = None

class CaregivingCreate(CaregivingBase):
    pass

class CaregivingResponse(CaregivingBase):
    id: int

    class Config:
        orm_mode = True