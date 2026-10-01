from typing import Generic,TypeVar
from pydantic import BaseModel
T=TypeVar('T')
class ErrorBody(BaseModel): code:str; message:str
class ApiResponse(BaseModel,Generic[T]): success:bool=True; data:T
class MessageResponse(BaseModel): success:bool=True; message:str
