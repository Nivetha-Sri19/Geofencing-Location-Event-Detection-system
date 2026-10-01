from types import SimpleNamespace
from decimal import Decimal
from app.geofencing.engine import haversine_m,classify_point,event_for_transition
from app.models.enums import GeofenceType,GeofenceState,GeofenceEventType

def circle(lat=0,lon=0,radius=100,tolerance=0):
    return SimpleNamespace(geofence_type=GeofenceType.CIRCLE,center_latitude=Decimal(str(lat)),center_longitude=Decimal(str(lon)),radius_meters=Decimal(str(radius)),boundary_tolerance_meters=Decimal(str(tolerance)),points=[])

def polygon(points,tolerance=0):
    return SimpleNamespace(geofence_type=GeofenceType.POLYGON,boundary_tolerance_meters=Decimal(str(tolerance)),points=[SimpleNamespace(latitude=Decimal(str(a)),longitude=Decimal(str(b))) for a,b in points])

def test_haversine_zero(): assert haversine_m(0,0,0,0)==0

def test_circle_center_inside(): assert classify_point(circle(radius=100),0,0)==GeofenceState.INSIDE

def test_circle_outside(): assert classify_point(circle(radius=100),0.01,0)==GeofenceState.OUTSIDE

def test_circle_tolerance(): assert classify_point(circle(radius=100,tolerance=20),0.00105,0)==GeofenceState.INSIDE

def test_polygon_inside(): assert classify_point(polygon([(0,0),(0,1),(1,1),(1,0)]),0.5,0.5)==GeofenceState.INSIDE

def test_polygon_outside(): assert classify_point(polygon([(0,0),(0,1),(1,1),(1,0)]),2,2)==GeofenceState.OUTSIDE

def test_polygon_edge_inside(): assert classify_point(polygon([(0,0),(0,1),(1,1),(1,0)]),0.5,0)==GeofenceState.INSIDE

def test_polygon_tolerance(): assert classify_point(polygon([(0,0),(0,1),(1,1),(1,0)],tolerance=120),0.5,-0.001)==GeofenceState.INSIDE

def test_transitions():
    assert event_for_transition(GeofenceState.OUTSIDE,GeofenceState.INSIDE)==GeofenceEventType.ENTER
    assert event_for_transition(GeofenceState.INSIDE,GeofenceState.OUTSIDE)==GeofenceEventType.EXIT
    assert event_for_transition(GeofenceState.INSIDE,GeofenceState.INSIDE)==GeofenceEventType.INSIDE
    assert event_for_transition(GeofenceState.OUTSIDE,GeofenceState.OUTSIDE)==GeofenceEventType.OUTSIDE
