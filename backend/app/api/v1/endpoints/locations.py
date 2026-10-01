from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.location import LocationSubmit,LocationProcessingResponse,EventHistoryItem,LocationHistoryItem
from app.services.location_service import LocationService
from app.models.enums import GeofenceEventType
router=APIRouter(prefix='/locations',tags=['Location Processing'])
@router.post('/process',response_model=LocationProcessingResponse)
async def process(data:LocationSubmit,db:AsyncSession=Depends(get_db),user=Depends(get_current_user)):
    location,events=await LocationService(db).process(data,user)
    return LocationProcessingResponse(location_event_id=location.id,device_id=location.device_id,latitude=float(location.latitude),longitude=float(location.longitude),timestamp=location.recorded_at,events=events)
@router.get('/events',response_model=list[EventHistoryItem])
async def events(device_id:int|None=None,geofence_id:int|None=None,event_type:GeofenceEventType|None=None,limit:int=100,offset:int=0,db:AsyncSession=Depends(get_db),user=Depends(get_current_user)):
    limit=min(max(limit,1),500); offset=max(offset,0); return await LocationService(db).history(user,device_id,geofence_id,event_type,limit,offset)

@router.get('/history',response_model=list[LocationHistoryItem])
async def location_history(device_id:int|None=None,limit:int=100,offset:int=0,db:AsyncSession=Depends(get_db),user=Depends(get_current_user)):
    return await LocationService(db).location_history(user,device_id,min(max(limit,1),500),max(offset,0))
@router.get('/current',response_model=list[LocationHistoryItem])
async def current_locations(db:AsyncSession=Depends(get_db),user=Depends(get_current_user)):
    return await LocationService(db).current_locations(user)
