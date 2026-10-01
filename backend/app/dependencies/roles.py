from fastapi import Depends,HTTPException
from app.dependencies.auth import get_current_user
from app.models.enums import UserRole
from app.models.user import User
def require_roles(*roles:UserRole):
    async def dependency(user:User=Depends(get_current_user)):
        if user.role not in roles: raise HTTPException(403,'Insufficient permissions')
        return user
    return dependency
