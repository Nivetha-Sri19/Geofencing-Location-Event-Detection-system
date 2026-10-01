from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.core.database import Base
if TYPE_CHECKING:
    from app.models.user import User
    from app.models.location_event import LocationEvent
    from app.models.geofence_event import GeofenceEvent
    from app.models.device_geofence_state import DeviceGeofenceState
class Device(Base):
    __tablename__='devices'
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey('users.id',ondelete='CASCADE'),index=True)
    device_identifier: Mapped[str]=mapped_column(String(150),unique=True,index=True)
    name: Mapped[str]=mapped_column(String(150))
    is_active: Mapped[bool]=mapped_column(Boolean,default=True,index=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
    user: Mapped['User']=relationship(back_populates='devices')
    locations: Mapped[list['LocationEvent']]=relationship(back_populates='device')
    geofence_events: Mapped[list['GeofenceEvent']]=relationship(back_populates='device')
    geofence_states: Mapped[list['DeviceGeofenceState']]=relationship(back_populates='device',cascade='all, delete-orphan')
