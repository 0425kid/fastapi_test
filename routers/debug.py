from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Relationship
from schemas import RelationshipResponse

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get(
    "/choi",
    summary="최지민 api입니다",
    description="실행하지 마세요",
    tags=["debug"]
)
async def choi():
    return {"최지민": "바보"}


# 모든 관계 정보 불러오기
@router.get(
    "/relationship",
    response_model=list[RelationshipResponse],
    summary="모든 관계 정보 불러오기",
)
def get_all_relationships(db: Session = Depends(get_db)):
    
    relationships = db.query(Relationship).all()
    return relationships