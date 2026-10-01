from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.dependencies.roles import require_roles
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.admin import UserAdminResponse,UserRoleUpdate,UserStatusUpdate
from app.services.audit_service import audit
router=APIRouter(prefix='/users',tags=['User Administration'])
@router.get('',response_model=list[UserAdminResponse])
async def list_users(db:AsyncSession=Depends(get_db),admin=Depends(require_roles(UserRole.ADMIN))): return list((await db.scalars(select(User).order_by(User.id.desc()))).all())
@router.patch('/{user_id}/role',response_model=UserAdminResponse)
async def change_role(user_id:int,data:UserRoleUpdate,db:AsyncSession=Depends(get_db),admin=Depends(require_roles(UserRole.ADMIN))):
    user=await db.get(User,user_id)
    if not user: raise HTTPException(404,'User not found')
    user.role=data.role; await audit(db,admin.id,'ROLE_UPDATED','user',user.id,{'role':data.role.value}); await db.commit(); await db.refresh(user); return user
@router.patch('/{user_id}/status',response_model=UserAdminResponse)
async def change_status(user_id:int,data:UserStatusUpdate,db:AsyncSession=Depends(get_db),admin=Depends(require_roles(UserRole.ADMIN))):
    user=await db.get(User,user_id)
    if not user: raise HTTPException(404,'User not found')
    if user.id==admin.id and not data.is_active: raise HTTPException(400,'Administrator cannot deactivate the current account')
    user.is_active=data.is_active; await audit(db,admin.id,'STATUS_UPDATED','user',user.id,{'is_active':data.is_active}); await db.commit(); await db.refresh(user); return user
