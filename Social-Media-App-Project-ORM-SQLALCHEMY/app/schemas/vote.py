from pydantic import BaseModel
from typing import Literal

class VoteBase(BaseModel):
    post_id: int
    dir: Literal[0,1]
    
class VoteResponse(VoteBase):
    pass