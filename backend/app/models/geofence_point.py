from decimal import Decimal
from sqlalchemy import ForeignKey,Numeric,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.core.database import Base
class GeofencePoint(Base):
    __tablename__='geofence_points'
    __table_args__=(UniqueConstraint('geofence_id','sequence',name='uq_geofence_point_sequence'),)
    id: Mapped[int]=mapped_column(primary_key=True)
    geofence_id: Mapped[int]=mapped_column(ForeignKey('geofences.id',ondelete='CASCADE'),index=True)
    sequence: Mapped[int]=mapped_column()
    latitude: Mapped[Decimal]=mapped_column(Numeric(10,7))
    longitude: Mapped[Decimal]=mapped_column(Numeric(10,7))
    geofence=relationship('Geofence',back_populates='points')
