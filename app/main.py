# FastAPI : fastAPI 프레임 워크
# Depends : 종속성 주입용
# HTTPException : 예외 처리
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# PostgreSQL database 연결 url
DATABASE_URL = "postgresql://myuser:password@localhost/mydatabase"

# SQLAlchemy database 엔진 생성
engine = create_engine(DATABASE_URL)

# SQLAlchemy session 생성기
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모든 SQLAlchemy models에 대한 base class
Base = declarative_base()

# 요양사 클래스
class Caregiver(Base):
    __tablename__ = "caregivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    address = Column(String, nullable=False)
    career = Column(Text)
    desired_hourly_rate = Column(Integer, nullable=False)

# Pydantic model for caregiver registration
class CaregiverCreate(BaseModel):
    name: str
    age: int
    gender: str
    phone_number: str
    address: str
    career: str
    desired_hourly_rate: int

# Pydantic model for caregiver response
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

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create caregiver API endpoint
@app.post("/caregivers/", response_model=CaregiverResponse)
def create_caregiver(caregiver: CaregiverCreate, db: Session = Depends(get_db)):
    db_caregiver = Caregiver(
        name=caregiver.name,
        age=caregiver.age,
        gender=caregiver.gender,
        phone_number=caregiver.phone_number,
        address=caregiver.address,
        career=caregiver.career,
        desired_hourly_rate=caregiver.desired_hourly_rate,
    )
    db.add(db_caregiver)
    db.commit()
    db.refresh(db_caregiver)
    return db_caregiver

