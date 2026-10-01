from datetime import datetime
from pydantic import BaseModel,Field,ConfigDict
class DeviceCreate(BaseModel): device_identifier:str=Field(min_length=2,max_length=150); name:str=Field(min_length=1,max_length=150); user_id:int|None=None
class DeviceUpdate(BaseModel): name:str|None=Field(default=None,min_length=1,max_length=150); is_active:bool|None=None; user_id:int|None=None
class DeviceResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int; user_id:int; device_identifier:str; name:str; is_active:bool; created_at:datetime; updated_at:datetime
