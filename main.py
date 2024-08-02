# main.py

from fastapi import FastAPI
from routers.debug import router as debug_router
from routers.account import router as account_router
from routers.caregiver import router as caregiver_router
from routers.guardian import router as guardian_router
from routers.profile import router as profile_router
from routers.message import router as message_router
from routers.caregiving import router as caregiving_router



app = FastAPI()

app.include_router(profile_router, prefix="/profile", tags=["profile"])
app.include_router(account_router, prefix="/account", tags=["account"])

app.include_router(caregiver_router, prefix="/caregivers", tags=["caregivers"])
app.include_router(guardian_router, prefix="/guardians", tags=["guardians"])

app.include_router(message_router, prefix="/message", tags=["message"])
app.include_router(caregiving_router, prefix="/caregiving", tags=["caregiving"])

app.include_router(debug_router, prefix="/debug", tags=["debug"])