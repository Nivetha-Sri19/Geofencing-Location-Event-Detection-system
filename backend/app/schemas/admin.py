from pydantic import BaseModel,Field,ConfigDict
from app.models.enums import UserRole
class UserAdminResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int; username:str; email:str; role:UserRole; is_active:bool
class UserRoleUpdate(BaseModel): role:UserRole
class UserStatusUpdate(BaseModel): is_active:bool
