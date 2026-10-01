from sqlalchemy.ext.asyncio import AsyncSession
from app.models.audit_log import AuditLog
async def audit(db:AsyncSession,user_id:int|None,action:str,entity_type:str,entity_id:int|None=None,details:dict|None=None):
    db.add(AuditLog(user_id=user_id,action=action,entity_type=entity_type,entity_id=str(entity_id) if entity_id is not None else None,details=details))
