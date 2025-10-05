from ..database import Base
from sqlalchemy import Column, Integer, String, Boolean, func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Post(Base): 
    __tablename__ = "posts"
    
    id = Column(Integer,nullable=False, primary_key = True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)  
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True, server_default="True")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=func.now())
    
    owner = relationship("User")