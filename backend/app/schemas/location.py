from datetime import datetime,timezone
from pydantic import BaseModel,Field,field_validator,ConfigDict
from app.models.enums import GeofenceEventType,GeofenceState
class LocationSubmit(BaseModel):
    device_id:int
    latitude:float=Field(ge=-90,le=90)
    longitude:float=Field(ge=-180,le=180)
    timestamp:datetime
    @field_validator('timestamp')
    @classmethod
    def timestamp_tz(cls,v:datetime):
        if v.tzinfo is None: raise ValueError('timestamp must include timezone information')
        return v.astimezone(timezone.utc)
class EventResult(BaseModel):
    geofence_id:int; geofence_name:str; event_type:GeofenceEventType; previous_state:GeofenceState; current_state:GeofenceState; timestamp:datetime
class LocationProcessingResponse(BaseModel):
    location_event_id:int; device_id:int; latitude:float; longitude:float; timestamp:datetime; events:list[EventResult]
class EventHistoryItem(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int; device_id:int; geofence_id:int; location_event_id:int; event_type:GeofenceEventType; previous_state:GeofenceState; current_state:GeofenceState; occurred_at:datetime
class LocationHistoryItem(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int; device_id:int; latitude:float; longitude:float; recorded_at:datetime; received_at:datetime
