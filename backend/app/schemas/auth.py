from pydantic import BaseModel,EmailStr,Field,ConfigDict
from app.models.enums import UserRole
class RegisterRequest(BaseModel):
    username:str=Field(min_length=3,max_length=100,pattern=r'^[A-Za-z0-9_.-]+$')
    email:EmailStr
    password:str=Field(min_length=8,max_length=128)
class LoginRequest(BaseModel): username:str=Field(min_length=3,max_length=100); password:str=Field(min_length=1,max_length=128)
class TokenResponse(BaseModel): access_token:str; token_type:str='bearer'; expires_in:int
class UserResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id:int; username:str; email:EmailStr; role:UserRole; is_active:bool
