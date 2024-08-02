from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionLocal
from models import Caregiver, CaregiverProfile
from schemas import CaregiverCreate, CaregiverResponse

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 신규 요양사 회원가입
@router.post(
    "/",
    # response_model=CaregiverResponse,
    summary="신규 요양사 회원가입",
    description="name, age, gender, phone, address, experience, desired hourly rate 를 입력받아 새 요양사 등록.",
    response_description="The created caregiver's details."
)
def create_caregiver(caregiver: CaregiverCreate, db: Session = Depends(get_db)):
    # caregiver 정보 생성
    db_caregiver = Caregiver(
        username=caregiver.username,
        email=caregiver.email,
        password=caregiver.password,
        name=caregiver.name,
        age=caregiver.age,
        gender=caregiver.gender,
        phone=caregiver.phone,
        address=caregiver.address,
        points=0,
    )
    try:
        db.add(db_caregiver)
        db.commit()
        db.refresh(db_caregiver)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"요양사 회원가입 실패: {str(e)}")

    # 빈 프로필 생성
    db_caregiver_profile = CaregiverProfile(
        caregiver_id=db_caregiver.id,
        experience_ids=[],
        desired_hourly_rate=None,
        activity_start_time=None,
        activity_end_time=None
    )
    try:
        db.add(db_caregiver_profile)
        db.commit()
        db.refresh(db_caregiver_profile)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"요양사의 빈 프로필 생성 실패: {str(e)}")

    return {"response": True}

# 모든 요양사 정보 불러오기
@router.get(
    "/",
    response_model=list[CaregiverResponse],
    summary="모든 요양사 정보 불러오기",
    description="caregivers 테이블에 있는 모든 데이터 반환"
)
def get_all_caregivers(db: Session = Depends(get_db)):
    caregivers = db.query(Caregiver).all()
    return caregivers

# 특정 요양사 정보 불러오기
@router.get(
    "/id/{caregiver_id}",
    response_model=CaregiverResponse,
    summary="index로 특정 요양사 정보 불러오기",
    description="Retrieve the details of a caregiver by their ID."
)
def get_caregiver(caregiver_id: int, db: Session = Depends(get_db)):
    caregiver = db.query(Caregiver).filter(Caregiver.id == caregiver_id).first()
    if caregiver is None:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    return caregiver

# 특정 요양사 정보 불러오기
@router.get(
    "/username/{caregiver_username}",
    response_model=CaregiverResponse,
    summary="username으로 특정 요양사 정보 불러오기",
    description="Retrieve the details of a caregiver by their username."
)
def get_caregiver(username: str, db: Session = Depends(get_db)):
    caregiver = db.query(Caregiver).filter(Caregiver.username == username).first()
    if caregiver is None:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    return caregiver

@router.get(
    "/count",
    summary="등록된 요양사 데이터의 수 반환"
)
def count_caregivers(db: Session = Depends(get_db)):
    count = db.query(Caregiver).count()
    return {"count": count}




# 모든 요양사 삭제 및 테이블 초기화
@router.delete(
    "/reset/",
    summary="모든 요양사 삭제 및 테이블 초기화",
    description="caregivers 테이블에 있는 모든 데이터를 삭제하고 테이블 초기화."
)
def delete_all_caregivers(db: Session = Depends(get_db)):
    try:
        # CaregiverProfile과 관련된 레코드를 먼저 삭제합니다
        db.query(CaregiverProfile).delete()
        db.commit()

        # Caregiver 테이블의 레코드를 삭제하고 자동 증가 column 초기화합니다
        db.query(Caregiver).delete()
        db.commit()

        # 자동 증가 column 초기화 (text() 함수 사용)
        db.execute(text('TRUNCATE TABLE caregivers RESTART IDENTITY CASCADE'))
        db.commit()
        
        return {"message": "요양사 테이블 초기화 완료"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete caregivers: {str(e)}")

