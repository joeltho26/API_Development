from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Union
        
class UserBase(BaseModel):
    email: EmailStr
    
class UserCreate(UserBase):
    password: str
    
class UserUpdate(UserCreate):
    pass

class UserReponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        
class UserCreateEmailExist(UserBase):
    error: str
    optional_field: Union[str, None] = None
        
# class UserReponseUpdate(UserBase):
#     id : int
#     updated_at: datetime
    
#     class Config:
#         from_attributes = True