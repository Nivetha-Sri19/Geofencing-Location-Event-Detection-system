from fastapi import HTTPException
from sqlalchemy import select,func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.device import Device
from app.models.location_event import LocationEvent
from app.models.geofence import Geofence
from app.models.geofence_event import GeofenceEvent
from app.models.device_geofence_state import DeviceGeofenceState
from app.models.enums import GeofenceState
from app.geofencing.engine import classify_point,event_for_transition
from app.schemas.location import LocationSubmit
class LocationService:
    def __init__(self,db:AsyncSession): self.db=db
    async def process(self,data:LocationSubmit,current_user):
        device=await self.db.get(Device,data.device_id)
        if not device or not device.is_active: raise HTTPException(404,'Active device not found')
        if current_user.role.value!='admin' and device.user_id!=current_user.id: raise HTTPException(403,'Device access denied')
        duplicate=await self.db.scalar(select(LocationEvent).where(LocationEvent.device_id==device.id,LocationEvent.recorded_at==data.timestamp,LocationEvent.latitude==data.latitude,LocationEvent.longitude==data.longitude))
        if duplicate: raise HTTPException(409,'Duplicate location submission')
        latest=await self.db.scalar(select(LocationEvent).where(LocationEvent.device_id==device.id).order_by(LocationEvent.recorded_at.desc()).limit(1))
        if latest and data.timestamp < latest.recorded_at: raise HTTPException(409,'Location timestamp is older than the latest recorded location')
        location=LocationEvent(device_id=device.id,latitude=data.latitude,longitude=data.longitude,recorded_at=data.timestamp)
        self.db.add(location); await self.db.flush()
        geofences=list((await self.db.scalars(select(Geofence).options(selectinload(Geofence.points)).where(Geofence.is_active.is_(True)))).all())
        results=[]
        for g in geofences:
            state=await self.db.scalar(select(DeviceGeofenceState).where(DeviceGeofenceState.device_id==device.id,DeviceGeofenceState.geofence_id==g.id).with_for_update())
            current=classify_point(g,data.latitude,data.longitude)
            if state is None:
                previous=GeofenceState.OUTSIDE
                state=DeviceGeofenceState(device_id=device.id,geofence_id=g.id,current_state=current,last_latitude=data.latitude,last_longitude=data.longitude,last_recorded_at=data.timestamp)
                self.db.add(state); await self.db.flush()
            else:
                previous=state.current_state
                state.current_state=current; state.last_latitude=data.latitude; state.last_longitude=data.longitude; state.last_recorded_at=data.timestamp
            event_type=event_for_transition(previous,current)
            if bool(g.event_rules.get(event_type.value,True)):
                self.db.add(GeofenceEvent(device_id=device.id,geofence_id=g.id,location_event_id=location.id,event_type=event_type,previous_state=previous,current_state=current,occurred_at=data.timestamp))
                results.append({'geofence_id':g.id,'geofence_name':g.name,'event_type':event_type,'previous_state':previous,'current_state':current,'timestamp':data.timestamp})
        await self.db.commit()
        return location,results
    async def history(self,current_user,device_id=None,geofence_id=None,event_type=None,limit=100,offset=0):
        q=select(GeofenceEvent).join(Device,Device.id==GeofenceEvent.device_id).where(True)
        if current_user.role.value!='admin': q=q.where(Device.user_id==current_user.id)
        if device_id is not None: q=q.where(GeofenceEvent.device_id==device_id)
        if geofence_id is not None: q=q.where(GeofenceEvent.geofence_id==geofence_id)
        if event_type is not None: q=q.where(GeofenceEvent.event_type==event_type)
        q=q.order_by(GeofenceEvent.occurred_at.desc()).offset(offset).limit(limit)
        return list((await self.db.scalars(q)).all())
    async def location_history(self,current_user,device_id:int|None=None,limit=100,offset=0):
        q=select(LocationEvent).join(Device).order_by(LocationEvent.recorded_at.desc()).offset(offset).limit(limit)
        if current_user.role.value!='admin': q=q.where(Device.user_id==current_user.id)
        if device_id is not None: q=q.where(LocationEvent.device_id==device_id)
        return list((await self.db.scalars(q)).all())
    async def current_locations(self,current_user):
        latest=select(LocationEvent.device_id,func.max(LocationEvent.recorded_at).label('latest')).group_by(LocationEvent.device_id).subquery()
        q=select(LocationEvent).join(latest,(LocationEvent.device_id==latest.c.device_id)&(LocationEvent.recorded_at==latest.c.latest)).join(Device,Device.id==LocationEvent.device_id)
        if current_user.role.value!='admin': q=q.where(Device.user_id==current_user.id)
        return list((await self.db.scalars(q)).all())
