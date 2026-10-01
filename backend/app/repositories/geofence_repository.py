from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.geofence import Geofence
class GeofenceRepository:
    def __init__(self,db:AsyncSession): self.db=db
    async def get(self,geofence_id:int): return await self.db.scalar(select(Geofence).options(selectinload(Geofence.points)).where(Geofence.id==geofence_id))
    async def active(self): return list((await self.db.scalars(select(Geofence).options(selectinload(Geofence.points)).where(Geofence.is_active.is_(True)).order_by(Geofence.id))).all())
    async def list(self): return list((await self.db.scalars(select(Geofence).options(selectinload(Geofence.points)).order_by(Geofence.id.desc()))).all())
