from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import decode_access_token
from app.repositories.user_repository import UserRepository
from app.models.user import User
security=HTTPBearer()
async def get_current_user(credentials:HTTPAuthorizationCredentials=Depends(security),db:AsyncSession=Depends(get_db))->User:
    try: payload=decode_access_token(credentials.credentials); user_id=int(payload['sub'])
    except Exception as exc: raise HTTPException(status.HTTP_401_UNAUTHORIZED,'Invalid or expired token') from exc
    user=await UserRepository(db).get_by_id(user_id)
    if not user or not user.is_active: raise HTTPException(status.HTTP_401_UNAUTHORIZED,'User is inactive or unavailable')
    return user
