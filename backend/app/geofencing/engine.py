from math import atan2,cos,pi,sin,sqrt
from app.models.enums import GeofenceState,GeofenceType
EARTH_RADIUS_M=6_371_008.8

def haversine_m(lat1,lon1,lat2,lon2):
    p1,p2=lat1*pi/180,lat2*pi/180; dp=(lat2-lat1)*pi/180; dl=(lon2-lon1)*pi/180
    a=sin(dp/2)**2+cos(p1)*cos(p2)*sin(dl/2)**2
    return 2*EARTH_RADIUS_M*atan2(sqrt(a),sqrt(max(0,1-a)))

def point_segment_distance_m(lat,lon,lat1,lon1,lat2,lon2):
    # Local equirectangular projection around the query point; accurate enough for short geofence boundaries.
    scale=pi/180*EARTH_RADIUS_M; c=cos(lat*pi/180)
    x=(lon-lon1)*scale*c; y=(lat-lat1)*scale
    x2=(lon2-lon1)*scale*c; y2=(lat2-lat1)*scale
    denom=x2*x2+y2*y2
    if denom==0: return haversine_m(lat,lon,lat1,lon1)
    t=max(0,min(1,(x*x2+y*y2)/denom)); px=t*x2; py=t*y2
    return sqrt((x-px)**2+(y-py)**2)

def point_in_polygon(lat,lon,points):
    inside=False
    n=len(points)
    for i in range(n):
        lat1,lon1=points[i]; lat2,lon2=points[(i+1)%n]
        if point_segment_distance_m(lat,lon,lat1,lon1,lat2,lon2)<=1e-9: return True
        intersects=((lat1>lat)!=(lat2>lat)) and (lon < (lon2-lon1)*(lat-lat1)/(lat2-lat1)+lon1)
        if intersects: inside=not inside
    return inside

def classify_point(geofence,lat,lon):
    tol=float(geofence.boundary_tolerance_meters or 0)
    if geofence.geofence_type==GeofenceType.CIRCLE:
        return GeofenceState.INSIDE if haversine_m(lat,lon,float(geofence.center_latitude),float(geofence.center_longitude)) <= float(geofence.radius_meters)+tol else GeofenceState.OUTSIDE
    pts=[(float(p.latitude),float(p.longitude)) for p in geofence.points]
    if point_in_polygon(lat,lon,pts): return GeofenceState.INSIDE
    if tol>0 and min(point_segment_distance_m(lat,lon,*a,*b) for a,b in zip(pts,pts[1:]+pts[:1]))<=tol: return GeofenceState.INSIDE
    return GeofenceState.OUTSIDE

def event_for_transition(previous,current):
    from app.models.enums import GeofenceEventType
    if previous==GeofenceState.OUTSIDE and current==GeofenceState.INSIDE: return GeofenceEventType.ENTER
    if previous==GeofenceState.INSIDE and current==GeofenceState.OUTSIDE: return GeofenceEventType.EXIT
    if current==GeofenceState.INSIDE: return GeofenceEventType.INSIDE
    return GeofenceEventType.OUTSIDE
