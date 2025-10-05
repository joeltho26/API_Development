from fastapi import status, HTTPException, Depends, Response, APIRouter
from ..schemas.user import UserReponse, UserCreate, UserUpdate, UserCreateEmailExist
from ..models.user import User
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Union
from ..utils import hash
from sqlalchemy.exc import IntegrityError
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# response_model=Union[UserReponse,UserCreateEmailExist]
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserReponse)
def create_user(userpayload: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash(userpayload.password)
    userpayload.password = hashed_password
    new_user = User(**userpayload.model_dump())
    user = db.query(User).filter(User.email==new_user.email).first()
    # try:
    if user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                        detail=f"user email: {new_user.email} already exist!")
    else:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    # except IntegrityError: => can try this approach too for email exists!
        # db.rollback()
        # return {"error": "Email already exists!", "email": new_user.email}

@router.get("/", response_model=List[UserReponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.get("/{id}", response_model=UserReponse)
def get_user(id: int, db: Session = Depends(get_db), 
             current_user: dict = Depends(get_current_user)):
    
    user = db.get(User,id)
    # post = db.query(model.Post).filter(model.Post.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with id {id} not found!")
    
    if user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to perform requested action")
        
    return user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id : int, db: Session = Depends(get_db), 
                current_user: dict = Depends(get_current_user)):
    
    # post = db.get(model.Post,id)
    # post = db.query(model.Post).filter(model.Post.id == id).first()
    user_query = db.query(User).filter(User.id == id)
    user = user_query.first() 
        
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with id {id} not found to delete!")
        
    if user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to perform requested action")
        
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=UserReponse)
def update_user(id: int, userpayload: UserUpdate, 
                db: Session = Depends(get_db), 
                current_user: dict = Depends(get_current_user)):
    
    user_query = db.query(User).where(User.id == id)
    user = user_query.first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found to update!")
        
    if user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to perform requested action")
        
    if userpayload.email != user.email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"given email with id {id} do not match for update!")
        
    hashed_password = hash(userpayload.password)
    userpayload.password = hashed_password
    user_query.update(userpayload.model_dump(), synchronize_session=False)
    db.commit()
    return user