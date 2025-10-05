from pydantic import BaseModel
from datetime import datetime
from .user import UserReponse

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass
    
class PostUpdate(BaseModel):
    title: str
    content: str

class PostReponse(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    owner: UserReponse
    
    class Config:
        from_attributes = True
        
class PostVoteReponse(BaseModel):
    post: PostReponse
    votes: int
    
    class Config:
        from_attributes = True
        
# class PostReponseUpdate(PostBase):
#     id : int
#     updated_at: datetime
    
#     class Config:
#         from_attributes = True