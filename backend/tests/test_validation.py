import pytest
from pydantic import ValidationError
from app.schemas.geofence import GeofenceCreate,PointInput
from app.models.enums import GeofenceType

def test_invalid_latitude():
    with pytest.raises(ValidationError): PointInput(latitude=91,longitude=0)

def test_circle_requires_parameters():
    with pytest.raises(ValidationError): GeofenceCreate(name='x',geofence_type=GeofenceType.CIRCLE)

def test_polygon_requires_three_points():
    with pytest.raises(ValidationError): GeofenceCreate(name='x',geofence_type=GeofenceType.POLYGON,points=[{'latitude':0,'longitude':0},{'latitude':1,'longitude':1}])
