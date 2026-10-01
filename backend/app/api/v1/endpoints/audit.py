from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.dependencies.roles import require_roles
from app.models.audit_log import AuditLog
from app.models.enums import UserRole

router=APIRouter(prefix="/audit-logs", tags=["Audit Logs"])

@router.get("")
async def list_audit_logs(limit:int=100, offset:int=0, db:AsyncSession=Depends(get_db), admin=Depends(require_roles(UserRole.ADMIN))):
    limit=min(max(limit,1),500); offset=max(offset,0)
    rows=list((await db.scalars(select(AuditLog).order_by(AuditLog.created_at.desc()).offset(offset).limit(limit))).all())
    return rows
