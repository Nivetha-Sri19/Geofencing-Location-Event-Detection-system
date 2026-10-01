from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.geofence import Geofence
from app.models.geofence_point import GeofencePoint
from app.models.enums import GeofenceType
from app.repositories.geofence_repository import GeofenceRepository
from app.schemas.geofence import GeofenceCreate,GeofenceUpdate
from app.core.config import settings
from app.services.audit_service import audit
class GeofenceService:
    def __init__(self,db:AsyncSession): self.db=db; self.repo=GeofenceRepository(db)
    async def create(self,data:GeofenceCreate,user_id:int):
        if data.geofence_type==GeofenceType.POLYGON and len(data.points)>settings.max_polygon_points: raise HTTPException(422,'Polygon has too many points')
        g=Geofence(name=data.name,description=data.description,geofence_type=data.geofence_type,center_latitude=data.center_latitude,center_longitude=data.center_longitude,radius_meters=data.radius_meters,boundary_tolerance_meters=data.boundary_tolerance_meters,event_rules=data.event_rules.model_dump(),is_active=data.is_active,created_by=user_id)
        self.db.add(g); await self.db.flush()
        for i,p in enumerate(data.points): self.db.add(GeofencePoint(geofence_id=g.id,sequence=i,latitude=p.latitude,longitude=p.longitude))
        await audit(self.db,user_id,'GEOFENCE_CREATED','geofence',g.id,{'name':g.name,'type':g.geofence_type.value}); await self.db.commit(); return await self.repo.get(g.id)
    async def list(self): return await self.repo.list()
    async def get(self,gid:int):
        g=await self.repo.get(gid)
        if not g: raise HTTPException(404,'Geofence not found')
        return g
    async def update(self,gid:int,data:GeofenceUpdate,user_id:int|None=None):
        g=await self.get(gid); values=data.model_dump(exclude_unset=True)
        points=values.pop('points',None); rules=values.pop('event_rules',None)
        if points is not None and g.geofence_type==GeofenceType.CIRCLE: raise HTTPException(422,'Circle geofences cannot contain polygon points')
        if rules is not None: g.event_rules=rules
        for k,v in values.items(): setattr(g,k,v)
        if points is not None:
            if g.geofence_type==GeofenceType.POLYGON and len(points)>settings.max_polygon_points: raise HTTPException(422,'Polygon has too many points')
            if g.geofence_type==GeofenceType.POLYGON and len(points)<3: raise HTTPException(422,'Polygon requires at least 3 points')
            g.points.clear(); await self.db.flush()
            for i,p in enumerate(points): self.db.add(GeofencePoint(geofence_id=g.id,sequence=i,latitude=p['latitude'],longitude=p['longitude']))
        await audit(self.db,user_id,'GEOFENCE_UPDATED','geofence',gid,values); await self.db.commit(); return await self.repo.get(gid)
    async def delete(self,gid:int):
        g=await self.get(gid); await self.db.delete(g); await audit(self.db,None,'GEOFENCE_DELETED','geofence',gid); await self.db.commit()
