from sqlalchemy.orm import Session
from . import models, schemas

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
