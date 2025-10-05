from jose import JWTError, jwt
from datetime import datetime, timedelta, UTC
from .schemas.token import Token, TokenData
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .database import get_db
from sqlalchemy.orm import Session
from .models.user import User
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    
    #copy of payload separate to encode
    to_encode = data.copy()
    
    #adding expiration
    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expiration_minutes)
    to_encode.update({'exp': expire})
    
    #signature
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token=token, key=settings.secret_key, algorithms=settings.algorithm)
        id = payload.get("user_id")
        
        if not id:
            raise credentials_exception
        
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data
        
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate":"Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.id == token.id).first()
    return user