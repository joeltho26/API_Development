from fastapi import Depends, APIRouter, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..utils import verify
from ..schemas.auth import Login
from ..schemas.token import Token
from ..models.user import User
from ..oauth2 import create_access_token

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    # Note:
    """while using OAuth2PasswordRequestForm, user_credentials.email field will be accessed as
    user_credentials.username
 
    testing: while testing via postmna => user form-data option instead of raw post requests
    """
    
    user = db.query(User).filter(User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Invalid Credentials!")
        
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Invalid Credentials!")
        
    # creating tokens for authentication
    access_token = create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
    