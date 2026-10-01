from fastapi import APIRouter,Depends,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_roles
from app.models.enums import UserRole
from app.schemas.geofence import GeofenceCreate,GeofenceUpdate,GeofenceResponse
from app.services.geofence_service import GeofenceService
router=APIRouter(prefix='/geofences',tags=['Geofences'])
@router.post('',response_model=GeofenceResponse,status_code=201)
async def create(data:GeofenceCreate,db:AsyncSession=Depends(get_db),user=Depends(require_roles(UserRole.ADMIN,UserRole.OPERATOR))): return await GeofenceService(db).create(data,user.id)
@router.get('',response_model=list[GeofenceResponse])
async def list_all(db:AsyncSession=Depends(get_db),user=Depends(get_current_user)): return await GeofenceService(db).list()
@router.get('/{geofence_id}',response_model=GeofenceResponse)
async def get_one(geofence_id:int,db:AsyncSession=Depends(get_db),user=Depends(get_current_user)): return await GeofenceService(db).get(geofence_id)
@router.patch('/{geofence_id}',response_model=GeofenceResponse)
async def update(geofence_id:int,data:GeofenceUpdate,db:AsyncSession=Depends(get_db),user=Depends(require_roles(UserRole.ADMIN,UserRole.OPERATOR))): return await GeofenceService(db).update(geofence_id,data,user.id)
@router.delete('/{geofence_id}',status_code=204)
async def delete(geofence_id:int,db:AsyncSession=Depends(get_db),user=Depends(require_roles(UserRole.ADMIN))): await GeofenceService(db).delete(geofence_id)
