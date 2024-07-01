from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas

def create_caregiver(db: Session, caregiver: schemas.CaregiverCreate):
    db_caregiver = models.Caregiver(
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

def update_caregiver(db: Session, caregiver_id: int, caregiver: schemas.CaregiverCreate):
    db_caregiver = db.query(models.Caregiver).filter(models.Caregiver.id == caregiver_id).first()
    if db_caregiver:
        db_caregiver.name = caregiver.name
        db_caregiver.age = caregiver.age
        db_caregiver.gender = caregiver.gender
        db_caregiver.phone_number = caregiver.phone_number
        db_caregiver.address = caregiver.address
        db_caregiver.career = caregiver.career
        db_caregiver.desired_hourly_rate = caregiver.desired_hourly_rate
        db.commit()
        db.refresh(db_caregiver)
    return db_caregiver

def get_caregivers(db: Session) -> List[models.Caregiver]:
    return db.query(models.Caregiver).all()

def get_caregiver(db: Session, caregiver_id: int) -> models.Caregiver:
    return db.query(models.Caregiver).filter(models.Caregiver.id == caregiver_id).first()
