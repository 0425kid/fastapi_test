from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# PostgreSQL database URL (replace with your actual database URL)
DATABASE_URL = "postgresql://myuser:password@localhost/mydatabase"

# SQLAlchemy database engine
engine = create_engine(DATABASE_URL)

# SQLAlchemy session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

# Caregiver model
class Caregiver(Base):
    __tablename__ = "caregivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String)
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

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create caregiver API endpoint
@app.post("/caregivers/", response_model=Caregiver)
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


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
