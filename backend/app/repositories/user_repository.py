from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
class UserRepository:
    def __init__(self,db:AsyncSession): self.db=db
    async def get_by_id(self,user_id:int): return await self.db.get(User,user_id)
    async def get_by_username(self,username:str): return await self.db.scalar(select(User).where(User.username==username))
    async def get_by_email(self,email:str): return await self.db.scalar(select(User).where(User.email==email))
    async def create(self,user:User): self.db.add(user); await self.db.flush(); await self.db.refresh(user); return user
