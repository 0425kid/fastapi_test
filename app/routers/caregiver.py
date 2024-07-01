from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models, database

router = APIRouter()

# 의존성 주입을 위한 데이터베이스 세션
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.CaregiverResponse)
def create_caregiver(caregiver: schemas.CaregiverCreate, db: Session = Depends(get_db)):
    return crud.create_caregiver(db=db, caregiver=caregiver)

@router.put("/{caregiver_id}", response_model=schemas.CaregiverResponse)
def update_caregiver(caregiver_id: int, caregiver: schemas.CaregiverCreate, db: Session = Depends(get_db)):
    db_caregiver = crud.get_caregiver(db, caregiver_id=caregiver_id)
    if db_caregiver is None:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    return crud.update_caregiver(db=db, caregiver_id=caregiver_id, caregiver=caregiver)

@router.get("/", response_model=List[schemas.CaregiverResponse])
def get_caregivers(db: Session = Depends(get_db)):
    return crud.get_caregivers(db)

@router.get("/{caregiver_id}", response_model=schemas.CaregiverResponse)
def get_caregiver(caregiver_id: int, db: Session = Depends(get_db)):
    db_caregiver = crud.get_caregiver(db, caregiver_id=caregiver_id)
    if db_caregiver is None:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    return db_caregiver
