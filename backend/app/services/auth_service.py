from fastapi import HTTPException,status
from app.core.security import hash_password,verify_password,create_access_token
from app.models.user import User
from app.models.enums import UserRole
from app.repositories.user_repository import UserRepository
class AuthService:
    def __init__(self,repo:UserRepository): self.repo=repo
    async def register(self,username,email,password):
        if await self.repo.get_by_username(username): raise HTTPException(409,'Username already exists')
        if await self.repo.get_by_email(email): raise HTTPException(409,'Email already exists')
        return await self.repo.create(User(username=username,email=email,password_hash=hash_password(password),role=UserRole.VIEWER))
    async def login(self,username,password):
        user=await self.repo.get_by_username(username)
        if not user or not verify_password(password,user.password_hash): raise HTTPException(status.HTTP_401_UNAUTHORIZED,'Invalid username or password')
        if not user.is_active: raise HTTPException(403,'User is inactive')
        return user,create_access_token(str(user.id),user.role.value)
