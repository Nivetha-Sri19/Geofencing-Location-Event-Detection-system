from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.device import Device
class DeviceRepository:
    def __init__(self,db:AsyncSession): self.db=db
    async def get(self,device_id:int): return await self.db.get(Device,device_id)
    async def get_by_identifier(self,identifier:str): return await self.db.scalar(select(Device).where(Device.device_identifier==identifier))
    async def list(self,owner_id:int|None=None):
        q=select(Device).order_by(Device.id.desc())
        if owner_id is not None: q=q.where(Device.user_id==owner_id)
        return list((await self.db.scalars(q)).all())
    async def create(self,device:Device): self.db.add(device); await self.db.flush(); await self.db.refresh(device); return device
