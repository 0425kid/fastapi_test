from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionLocal
from models import Guardian, Relationship
from schemas import GuardianCreate, GuardianResponse, RelationshipResponse

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 신규 보호자 등록
@router.post(
    "/",
    summary="신규 보호자 등록",
    description="name, age, gender, phone, address, relationship_index를 입력받아 새 보호자 등록.",
)
def create_guardian(guardian: GuardianCreate, db: Session = Depends(get_db)):
    db_guardian = Guardian(
        username = guardian.username,
        email = guardian.email,
        password = guardian.password,

        name=guardian.name,
        age=guardian.age,
        gender=guardian.gender,
        phone=guardian.phone,
        address=guardian.address,

        points = 0,
        relationship_index=guardian.relationship_index,
        service_urgency_index=guardian.service_urgency_index
    )

    db.add(db_guardian)
    db.commit()
    db.refresh(db_guardian)
    return {"response": True}

# 모든 보호자 정보 불러오기
@router.get(
    "/",
    response_model=list[GuardianResponse],
    summary="모든 보호자 정보 불러오기",
    description="guardians 테이블에 있는 모든 데이터 반환"
)
def get_all_guardians(db: Session = Depends(get_db)):
    guardians = db.query(Guardian).all()
    guardian_responses = []
    for guardian in guardians:
        relationship = db.query(Relationship).filter(Relationship.id == guardian.relationship_index).first()
        if relationship is None:
            raise HTTPException(status_code=404, detail=f"보호자 {guardian.id}의 관계 정보를 찾을 수 없습니다.")
        
        guardian_response = GuardianResponse(
            id = guardian.id,
            username = guardian.username,
            email = guardian.email,
            password = guardian.password,

            name=guardian.name,
            age=guardian.age,
            gender=guardian.gender,
            phone=guardian.phone,
            address=guardian.address,

            points = guardian.points,
            relationship=relationship.relationship_type,
            service_urgency_index=guardian.service_urgency_index
        )
        guardian_responses.append(guardian_response)
    
    return guardian_responses

# 특정 보호자 정보 불러오기
@router.get(
    "/id/{guardian_id}",
    response_model=GuardianResponse,
    summary="특정 보호자 정보 불러오기",
    description="Retrieve the details of a guardian by their ID."
)
def get_guardian(guardian_id: int, db: Session = Depends(get_db)):
    guardian = db.query(Guardian).filter(Guardian.id == guardian_id).first()
    if guardian is None:
        raise HTTPException(status_code=404, detail="Guardian not found")
    
    # 관계 정보를 가져오기
    relationship = db.query(Relationship).filter(Relationship.id == guardian.relationship_index).first()
    if relationship is None:
        raise HTTPException(status_code=404, detail="해당 인덱스의 보호자 찾지 못함")
    
    guardian_response = GuardianResponse(
        id = guardian.id,
        username = guardian.username,
        email = guardian.email,
        password = guardian.password,

        name=guardian.name,
        age=guardian.age,
        gender=guardian.gender,
        phone=guardian.phone,
        address=guardian.address,

        points = guardian.points,
        relationship=relationship.relationship_type,
        service_urgency_index=guardian.service_urgency_index
    )

    return guardian_response

@router.get(
    "/username/{guardian_username}",
    response_model=GuardianResponse,
    summary="username 보호자 정보 불러오기",
    description="Retrieve the details of a guardian by their username."
)
def get_guardian(username: str, db: Session = Depends(get_db)):
    guardian = db.query(Guardian).filter(Guardian.username == username).first()
    if guardian is None:
        raise HTTPException(status_code=404, detail="Guardian not found")
    
    # 관계 정보를 가져오기
    relationship = db.query(Relationship).filter(Relationship.id == guardian.relationship_index).first()
    if relationship is None:
        raise HTTPException(status_code=404, detail="해당 username의 보호자 찾지 못함")
    
    guardian_response = GuardianResponse(
        id = guardian.id,
        username = guardian.username,
        email = guardian.email,
        password = guardian.password,

        name=guardian.name,
        age=guardian.age,
        gender=guardian.gender,
        phone=guardian.phone,
        address=guardian.address,

        points = guardian.points,
        relationship=relationship.relationship_type,
        service_urgency_index=guardian.service_urgency_index
    )

    return guardian_response


# 모든 보호자 삭제 및 테이블 초기화
@router.delete(
    "/reset/",
    summary="모든 보호자 삭제 및 테이블 초기화",
    description="guardians 테이블에 있는 모든 데이터를 삭제하고 테이블 초기화."
)
def delete_all_guardians(db: Session = Depends(get_db)):
    try:
        # 데이터 삭제
        db.query(Guardian).delete()
        db.commit()
        
        # 자동 증가 column 초기화 (text() 함수 사용)
        db.execute(text('TRUNCATE TABLE guardians RESTART IDENTITY CASCADE'))
        db.commit()
        
        return {"message": "모든 보호자 정보 삭제 및 테이블 초기화 완료"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete guardians: {str(e)}")

