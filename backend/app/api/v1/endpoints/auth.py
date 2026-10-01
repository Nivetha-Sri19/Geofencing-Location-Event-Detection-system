from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.auth import RegisterRequest,LoginRequest,TokenResponse,UserResponse
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.dependencies.auth import get_current_user
router=APIRouter(prefix='/auth',tags=['Authentication'])
@router.post('/register',response_model=UserResponse,status_code=201)
async def register(data:RegisterRequest,db:AsyncSession=Depends(get_db)): return await AuthService(UserRepository(db)).register(data.username,data.email,data.password)
@router.post('/login',response_model=TokenResponse)
async def login(data:LoginRequest,db:AsyncSession=Depends(get_db)):
    user,token=await AuthService(UserRepository(db)).login(data.username,data.password); return TokenResponse(access_token=token,expires_in=60*60)
@router.get('/me',response_model=UserResponse)
async def me(user=Depends(get_current_user)): return user
