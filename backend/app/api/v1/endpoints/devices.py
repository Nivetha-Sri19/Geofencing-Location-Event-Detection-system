from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_roles
from app.models.enums import UserRole
from app.schemas.device import DeviceCreate,DeviceUpdate,DeviceResponse
from app.services.device_service import DeviceService
router=APIRouter(prefix='/devices',tags=['Devices'])
@router.post('',response_model=DeviceResponse,status_code=201)
async def create(data:DeviceCreate,db:AsyncSession=Depends(get_db),user=Depends(get_current_user)): return await DeviceService(db).create(data,user)
@router.get('',response_model=list[DeviceResponse])
async def list_devices(db:AsyncSession=Depends(get_db),user=Depends(get_current_user)): return await DeviceService(db).list(user)
@router.patch('/{device_id}',response_model=DeviceResponse)
async def update(device_id:int,data:DeviceUpdate,db:AsyncSession=Depends(get_db),user=Depends(get_current_user)): return await DeviceService(db).update(device_id,data,user)
