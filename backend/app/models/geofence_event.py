from datetime import datetime
from sqlalchemy import DateTime,Enum,ForeignKey,Index,UniqueConstraint,func
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.core.database import Base
from app.models.enums import GeofenceEventType,GeofenceState
class GeofenceEvent(Base):
    __tablename__='geofence_events'
    __table_args__=(Index('ix_geofence_events_lookup','device_id','geofence_id','occurred_at'),UniqueConstraint('location_event_id','geofence_id','event_type',name='uq_geofence_event_transition'))
    id: Mapped[int]=mapped_column(primary_key=True)
    device_id: Mapped[int]=mapped_column(ForeignKey('devices.id',ondelete='CASCADE'),index=True)
    geofence_id: Mapped[int]=mapped_column(ForeignKey('geofences.id',ondelete='CASCADE'),index=True)
    location_event_id: Mapped[int]=mapped_column(ForeignKey('location_events.id',ondelete='CASCADE'),index=True)
    event_type: Mapped[GeofenceEventType]=mapped_column(Enum(GeofenceEventType),index=True)
    previous_state: Mapped[GeofenceState]=mapped_column(Enum(GeofenceState))
    current_state: Mapped[GeofenceState]=mapped_column(Enum(GeofenceState))
    occurred_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),index=True)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    device=relationship('Device',back_populates='geofence_events')
    geofence=relationship('Geofence',back_populates='events')
    location_event=relationship('LocationEvent')
