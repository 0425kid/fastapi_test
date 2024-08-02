from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionLocal
from models import Caregiving
from schemas import CaregivingCreate, CaregivingResponse

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
        "/", 
        summary="모든 요양 신청 정보 불러오기",
        description=" " 
        )
def get_all_caregivings(db: Session = Depends(get_db)):
    caregivings = db.query(Caregiving).all()
    return caregivings


@router.post(
        "/", 
        summary="새 요양 신청",
        description=" " 
        )
def create_caregiving(caregiving: CaregivingCreate, db: Session = Depends(get_db)):
    try:
        db_caregiving = Caregiving(
            username = caregiving.username,

            start_date = caregiving.start_date,
            end_date = caregiving.end_date,
            care_days = caregiving.care_days,

            start_time = caregiving.start_time,
            end_time = caregiving.end_time,

            extra_days = caregiving.extra_days,
            address = caregiving.address,

            medications = caregiving.medications,
            note = caregiving.note,

            urgent_fee = caregiving.urgent_fee,
            severe_fee = caregiving.severe_fee



        )
        db.add(db_caregiving)
        db.commit()
        db.refresh(db_caregiving)
        return db_caregiving
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"요양 정보 등록 실패: {str(e)}")
    

# 모든 요양 정보 삭제 및 테이블 초기화
@router.delete(
    "/reset/",
    summary="모든 요양 정보 삭제 및 테이블 초기화",
    description="caregivers 테이블에 있는 모든 데이터를 삭제하고 테이블 초기화."
)
def delete_all_caregivers(db: Session = Depends(get_db)):
    try:
        db.query(Caregiving).delete()
        db.commit()

        db.execute(text('TRUNCATE TABLE caregiving RESTART IDENTITY CASCADE'))
        db.commit()
        
        return {"message": "요양 신청 테이블 초기화 완료"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"요양 정보 삭제 실패: {str(e)}")