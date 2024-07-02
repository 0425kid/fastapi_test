# 각종 import
# Depends : 종속성 주입
# HTTPException : 예외처리
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Caregiver, Base
from schemas import CaregiverCreate, CaregiverResponse

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 신규 요양사 회원가입
@app.post("/caregivers/", response_model=CaregiverResponse)
def create_caregiver(caregiver: CaregiverCreate, db: Session = Depends(get_db)):
    db_caregiver = Caregiver(
        name=caregiver.name,
        age=caregiver.age,
        gender=caregiver.gender,
        phone=caregiver.phone,
        address=caregiver.address,
        experience=caregiver.experience,
        desired_hourly_rate=caregiver.desired_hourly_rate,
    )
    db.add(db_caregiver)
    db.commit()
    db.refresh(db_caregiver)
    return db_caregiver

# 모든 요양사 정보 불러오기
@app.get("/caregivers/", response_model=list[CaregiverResponse])
def get_all_caregivers(db: Session = Depends(get_db)):
    caregivers = db.query(Caregiver).all()
    return caregivers

# Get a caregiver by index
@app.get("/caregivers/{caregiver_id}", response_model=CaregiverResponse)
def get_caregiver(caregiver_id: int, db: Session = Depends(get_db)):
    caregiver = db.query(Caregiver).filter(Caregiver.id == caregiver_id).first()
    if caregiver is None:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    return caregiver


# 모든 요양사 삭제 및 테이블 초기화
@app.delete("/caregivers/reset/")
def delete_all_caregivers(db: Session = Depends(get_db)):
    try:
        db.query(Caregiver).delete()
        db.commit()
        return {"message": "All caregivers deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete caregivers: {str(e)}")