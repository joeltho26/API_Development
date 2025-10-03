from fastapi import status, HTTPException, Depends, Response, APIRouter
from ..schemas.post import PostCreate, PostUpdate, PostReponse
from ..model import Post
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[PostReponse])
def get_posts(db: Session = Depends(get_db), 
              current_user: dict = Depends(get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    # posts = db.query(Post).all()
    posts = db.query(Post).filter(Post.title.contains(search)).limit(limit).offset(skip).all()
    # db.execute("""SELECT * FROM posts""")
    # posts = db.fetchall()
    # posts = db.query(Post).filter(Post.owner_id == current_user.id).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostReponse)
def create_post(payload: PostCreate, db: Session = Depends(get_db), 
                current_user: dict = Depends(get_current_user)):
    
    # with user authentication
    """
    in create post api in postman with data in the body of the request
    in addition to it we will add "Authorization" = "Bearer <JWT token> under form-data section"
    """
    data = payload.model_dump()
    data.update({"owner_id":current_user.id})
    new_post = Post(**data) 
    # new_post = model.Post(title=payload.title, content=payload.content, published=payload.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/latest", response_model=PostReponse)
def get_latest_post(db: Session = Depends(get_db), 
                    current_user: dict = Depends(get_current_user)):
    
    posts = db.query(Post).all()
    for post in posts:
        pass
    return post

@router.get("/{id}", response_model=PostReponse)
def get_post(id: int, db: Session = Depends(get_db), 
             current_user: dict = Depends(get_current_user)):
    
    post = db.get(Post,id)
    # post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found!")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db), 
                current_user: dict = Depends(get_current_user)):
    
    # post = db.get(model.Post,id)
    # post = db.query(model.Post).filter(model.Post.id == id).first()
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found to delete!")
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=PostReponse)
def update_post(id: int, payload: PostUpdate, db: Session = Depends(get_db), 
                current_user: dict = Depends(get_current_user)):
    
    post_query = db.query(Post).where(Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found to update!")
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to perform requested action")
        
    post_query.update(payload.model_dump(), synchronize_session=False)
    db.commit()
    return post