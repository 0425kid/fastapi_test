from fastapi import FastAPI
from .routers import caregiver
# from .routers import caregiver, patient, message

app = FastAPI()

# Include routers
app.include_router(caregiver.router, prefix="/caregivers", tags=["caregivers"])
# app.include_router(patient.router, prefix="/patients", tags=["patients"])
# app.include_router(message.router, prefix="/messages", tags=["messages"])
