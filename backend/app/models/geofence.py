from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import Boolean,DateTime,Enum,JSON,Numeric,String,func
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.core.database import Base
from app.models.enums import GeofenceType
if TYPE_CHECKING:
    from app.models.geofence_point import GeofencePoint
    from app.models.geofence_event import GeofenceEvent
    from app.models.device_geofence_state import DeviceGeofenceState
class Geofence(Base):
    __tablename__='geofences'
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(150),index=True)
    description: Mapped[str|None]=mapped_column(String(500),nullable=True)
    geofence_type: Mapped[GeofenceType]=mapped_column(Enum(GeofenceType),index=True)
    center_latitude: Mapped[Decimal|None]=mapped_column(Numeric(10,7),nullable=True)
    center_longitude: Mapped[Decimal|None]=mapped_column(Numeric(10,7),nullable=True)
    radius_meters: Mapped[Decimal|None]=mapped_column(Numeric(12,2),nullable=True)
    boundary_tolerance_meters: Mapped[Decimal]=mapped_column(Numeric(10,2),default=10,nullable=False)
    event_rules: Mapped[dict]=mapped_column(JSON,default=lambda:{'enter':True,'exit':True,'inside':True,'outside':True},nullable=False)
    is_active: Mapped[bool]=mapped_column(Boolean,default=True,index=True)
    created_by: Mapped[int|None]=mapped_column(nullable=True,index=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
    points: Mapped[list['GeofencePoint']]=relationship(back_populates='geofence',cascade='all, delete-orphan',order_by='GeofencePoint.sequence')
    events: Mapped[list['GeofenceEvent']]=relationship(back_populates='geofence')
    device_states: Mapped[list['DeviceGeofenceState']]=relationship(back_populates='geofence',cascade='all, delete-orphan')
