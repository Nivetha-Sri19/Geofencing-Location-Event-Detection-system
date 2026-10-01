from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.device import Device
from app.repositories.device_repository import DeviceRepository
from app.repositories.user_repository import UserRepository
from app.services.audit_service import audit
class DeviceService:
    def __init__(self,db:AsyncSession): self.db=db; self.repo=DeviceRepository(db); self.users=UserRepository(db)
    async def create(self,data,current):
        owner=data.user_id or current.id
        if current.role.value!='admin' and owner!=current.id: raise HTTPException(403,'You can only create devices for yourself')
        if not await self.users.get_by_id(owner): raise HTTPException(404,'User not found')
        if await self.repo.get_by_identifier(data.device_identifier): raise HTTPException(409,'Device identifier already exists')
        d=await self.repo.create(Device(user_id=owner,device_identifier=data.device_identifier,name=data.name)); await audit(self.db,current.id,'DEVICE_CREATED','device',d.id,{'device_identifier':d.device_identifier}); await self.db.commit(); return d
    async def list(self,current): return await self.repo.list(None if current.role.value=='admin' else current.id)
    async def update(self,device_id,data,current):
        d=await self.repo.get(device_id)
        if not d: raise HTTPException(404,'Device not found')
        if current.role.value!='admin' and d.user_id!=current.id: raise HTTPException(403,'Device access denied')
        for k,v in data.model_dump(exclude_unset=True).items():
            if k=='user_id' and current.role.value!='admin': raise HTTPException(403,'Only administrators can reassign devices')
            setattr(d,k,v)
        await audit(self.db,current.id,'DEVICE_UPDATED','device',d.id,data.model_dump(exclude_unset=True)); await self.db.commit(); await self.db.refresh(d); return d
