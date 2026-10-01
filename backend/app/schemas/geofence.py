from decimal import Decimal
from pydantic import BaseModel,Field,ConfigDict,model_validator
from app.models.enums import GeofenceType
class PointInput(BaseModel): latitude:float=Field(ge=-90,le=90); longitude:float=Field(ge=-180,le=180)
class EventRules(BaseModel): enter:bool=True; exit:bool=True; inside:bool=True; outside:bool=True
class GeofenceCreate(BaseModel):
    name:str=Field(min_length=1,max_length=150); description:str|None=Field(default=None,max_length=500); geofence_type:GeofenceType
    center_latitude:float|None=Field(default=None,ge=-90,le=90); center_longitude:float|None=Field(default=None,ge=-180,le=180)
    radius_meters:float|None=Field(default=None,gt=0,le=20_000_000); boundary_tolerance_meters:float=Field(default=10,ge=0,le=10000)
    points:list[PointInput]=Field(default_factory=list); event_rules:EventRules=Field(default_factory=EventRules); is_active:bool=True
    @model_validator(mode='after')
    def validate_shape(self):
        if self.geofence_type==GeofenceType.CIRCLE and (self.center_latitude is None or self.center_longitude is None or self.radius_meters is None): raise ValueError('Circle requires center latitude, center longitude and radius_meters')
        if self.geofence_type==GeofenceType.POLYGON and len(self.points)<3: raise ValueError('Polygon requires at least 3 points')
        if self.geofence_type==GeofenceType.CIRCLE and self.points: raise ValueError('Circle cannot contain polygon points')
        if self.geofence_type==GeofenceType.POLYGON and any(x is not None for x in [self.center_latitude,self.center_longitude,self.radius_meters]): raise ValueError('Polygon cannot contain circle fields')
        return self
class GeofenceUpdate(BaseModel):
    name:str|None=Field(default=None,min_length=1,max_length=150); description:str|None=Field(default=None,max_length=500); boundary_tolerance_meters:float|None=Field(default=None,ge=0,le=10000); event_rules:EventRules|None=None; is_active:bool|None=None; points:list[PointInput]|None=None; radius_meters:float|None=Field(default=None,gt=0,le=20_000_000); center_latitude:float|None=Field(default=None,ge=-90,le=90); center_longitude:float|None=Field(default=None,ge=-180,le=180)
class GeofencePointResponse(BaseModel): model_config=ConfigDict(from_attributes=True); sequence:int; latitude:Decimal; longitude:Decimal
class GeofenceResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int; name:str; description:str|None; geofence_type:GeofenceType; center_latitude:Decimal|None; center_longitude:Decimal|None; radius_meters:Decimal|None; boundary_tolerance_meters:Decimal; event_rules:dict; is_active:bool; points:list[GeofencePointResponse]
