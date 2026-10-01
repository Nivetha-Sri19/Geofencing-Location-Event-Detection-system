from datetime import datetime
from decimal import Decimal
from sqlalchemy import DateTime,ForeignKey,Index,Numeric,UniqueConstraint,func
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.core.database import Base
class LocationEvent(Base):
    __tablename__='location_events'
    __table_args__=(Index('ix_location_events_device_recorded','device_id','recorded_at'),UniqueConstraint('device_id','recorded_at','latitude','longitude',name='uq_location_duplicate'))
    id: Mapped[int]=mapped_column(primary_key=True)
    device_id: Mapped[int]=mapped_column(ForeignKey('devices.id',ondelete='CASCADE'),index=True)
    latitude: Mapped[Decimal]=mapped_column(Numeric(10,7))
    longitude: Mapped[Decimal]=mapped_column(Numeric(10,7))
    recorded_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),index=True)
    received_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
    device=relationship('Device',back_populates='locations')
