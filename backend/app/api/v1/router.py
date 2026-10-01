from fastapi import APIRouter
from app.api.v1.endpoints import auth,devices,geofences,locations,users,audit
router=APIRouter()
router.include_router(auth.router)
router.include_router(devices.router)
router.include_router(geofences.router)
router.include_router(locations.router)
router.include_router(users.router)
router.include_router(audit.router)
