from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.enums import UserRole
if TYPE_CHECKING:
    from app.models.device import Device
    from app.models.audit_log import AuditLog
class User(Base):
    __tablename__="users"
    id: Mapped[int]=mapped_column(primary_key=True)
    username: Mapped[str]=mapped_column(String(100),unique=True,index=True)
    email: Mapped[str]=mapped_column(String(255),unique=True,index=True)
    password_hash: Mapped[str]=mapped_column(String(255))
    role: Mapped[UserRole]=mapped_column(Enum(UserRole),default=UserRole.VIEWER,index=True)
    is_active: Mapped[bool]=mapped_column(Boolean,default=True,index=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
    devices: Mapped[list['Device']]=relationship(back_populates='user',cascade='all, delete-orphan')
    audit_logs: Mapped[list['AuditLog']]=relationship(back_populates='user')
