from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionLocal
from models import Caregiver, Guardian

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/check-email",
    summary="이메일 중복체크",
    description="사용가능한 이메일이면 true, 중복되는 닉네임이면 false를 반환",
)
async def check_nickname(email: str, db: Session = Depends(get_db)):
    # caregiver 테이블에 존재하는 이메일인지 확인
    caregiver = db.query(Caregiver).filter(Caregiver.email == email).first()

    if caregiver:
        return {"is_unique": False}
    
    # guardian 테이블에 존재하는 닉네임인지 확인
    guardian = db.query(Guardian).filter(Guardian.email == email).first()

    if guardian:
        return {"is_unique": False}

    return {"is_unique": True}      


@router.get(
    "/check-username",
    summary="유저 이름 중복체크",
    description="사용가능한 닉네임이면 true, 중복되는 닉네임이면 false를 반환",
)
async def check_nickname(username: str, db: Session = Depends(get_db)):
    # caregiver 테이블에 존재하는 닉네임인지 확인
    caregiver = db.query(Caregiver).filter(Caregiver.username == username).first()

    if caregiver:
        return {"is_unique": False}
    
    # guardian 테이블에 존재하는 닉네임인지 확인
    guardian = db.query(Guardian).filter(Guardian.username == username).first()

    if guardian:
        return {"is_unique": False}
    return {"is_unique": True}

