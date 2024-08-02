from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionLocal
from models import Caregiver, CaregiverProfile
from schemas import CaregiverProfileResponse, CaregiverProfileUpdate

router = APIRouter()




# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_id(username: str, db):
    user = db.query(Caregiver).filter(Caregiver.username == username).first()
    if user is None:
        return None
    return user.id

@router.get(
    "/caregivers",
    summary="모든 요양사 프로필 불러오기",
    description="모든 요양사의 프로필을 가져옴",
    response_description="요양사 프로필 목록"
)
def get_caregiver_profile(db: Session = Depends(get_db)):
    profiles = db.query(CaregiverProfile).all()
    return profiles
    #profiles = db.query(Caregiver).all()

@router.post(
    "/caregivers",
    summary="해당하는 이름에 대한 요양사 프로필 불러오기",
)
def get_caregiver_profile_by_name(username: str, db: Session = Depends(get_db)):
    #user = db.query(Caregiver).filter(Caregiver.username == username).first()
    caregiver_id = get_user_id(username, db)

    if caregiver_id is None: 
        raise HTTPException(status_code=404, detail="해당 이름을 가진 요양사가 존재하지 않음")
    
    profile = db.query(CaregiverProfile).filter(CaregiverProfile.caregiver_id == caregiver_id).first()
    
    if profile is None:
        raise HTTPException(status_code=404, detail="해당 요양사의 프로필이 존재하지 않음")
    
    return profile

# 요양사 프로필 업데이트
@router.post(
    "/update",
    summary="해당하는 유저 이름에 대한 요양사 프로필 업데이트",
)
def update_caregiver_profile(profile_data: CaregiverProfileUpdate, db: Session = Depends(get_db)):
    caregiver_id = get_user_id(profile_data.username, db)

    if caregiver_id is None: 
        raise HTTPException(status_code=404, detail="해당 이름을 가진 요양사가 존재하지 않음")
    
    try:
        profile = db.query(CaregiverProfile).filter(CaregiverProfile.caregiver_id == caregiver_id).first()
        if profile is None:
            raise HTTPException(status_code=404, detail="해당 요양사의 프로필을 찾을 수 없음")
        
        profile.experience_ids = profile_data.experience_ids
        profile.desired_hourly_rate = profile_data.desired_hourly_rate
        profile.activity_start_time = profile_data.activity_start_time
        profile.activity_end_time = profile_data.activity_end_time
        
        db.commit()
        db.refresh(profile)
        
        return profile_data
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"프로필 업데이트 실패: {str(e)}")

