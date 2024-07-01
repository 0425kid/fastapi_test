from fastapi import FastAPI
from app.routers import caregiver, patient, message  # 절대 경로 사용

app = FastAPI()

# Include routers
app.include_router(caregiver.router, prefix="/caregivers", tags=["caregivers"])
# app.include_router(patient.router, prefix="/patients", tags=["patients"])
# app.include_router(message.router, prefix="/messages", tags=["messages"])
