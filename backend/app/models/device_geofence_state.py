from datetime import datetime
from decimal import Decimal
from sqlalchemy import DateTime,Enum,ForeignKey,Numeric,UniqueConstraint,func
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.core.database import Base
from app.models.enums import GeofenceState
class DeviceGeofenceState(Base):
    __tablename__='device_geofence_states'
    __table_args__=(UniqueConstraint('device_id','geofence_id',name='uq_device_geofence_state'),)
    id: Mapped[int]=mapped_column(primary_key=True)
    device_id: Mapped[int]=mapped_column(ForeignKey('devices.id',ondelete='CASCADE'),index=True)
    geofence_id: Mapped[int]=mapped_column(ForeignKey('geofences.id',ondelete='CASCADE'),index=True)
    current_state: Mapped[GeofenceState]=mapped_column(Enum(GeofenceState))
    last_latitude: Mapped[Decimal]=mapped_column(Numeric(10,7))
    last_longitude: Mapped[Decimal]=mapped_column(Numeric(10,7))
    last_recorded_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),index=True)
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
    device=relationship('Device',back_populates='geofence_states')
    geofence=relationship('Geofence',back_populates='device_states')
