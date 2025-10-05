from fastapi import status, HTTPException, Depends, Response, APIRouter
from ..schemas.post import PostCreate, PostUpdate, PostReponse, PostVoteReponse
from ..models.post import Post
from ..models.vote import Vote
from ..database import get_db
from sqlalchemy.orm import Session, aliased
from typing import List, Optional
from ..oauth2 import get_current_user
from sqlalchemy import func, desc

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# response_model=List[PostVoteReponse]
@router.get("/", response_model=List[PostVoteReponse])
def get_posts(db: Session = Depends(get_db), 
              limit: int = 10, 
              skip: int = 0, 
              search: Optional[str] = ""):
    
    # posts = db.query(Post).all()
    # posts = db.query(Post).filter(Post.title.contains(search)).limit(limit).offset(skip).all()
    # db.execute("""SELECT * FROM posts""")
    # posts = db.fetchall()
    # posts = db.query(Post).filter(Post.owner_id == current_user.id).all()
    alias_post = aliased(Post, name='post')
    posts = db.query(alias_post, func.count(Vote.post_id).label("votes")).join(Vote,Vote.post_id == alias_post.id, isouter=True).group_by(alias_post.id).filter(alias_post.title.contains(search)).limit(limit).offset(skip).all()
    
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

# response_model=PostReponse
@router.get("/latest", response_model=List[PostVoteReponse])
def get_latest_post(db: Session = Depends(get_db),
                    limit: int = 3):
    
    # posts = db.query(Post).all()
    alias_post = aliased(Post, name='post')
    posts = db.query(alias_post, func.count(Vote.post_id).label("votes")).join(Vote,Vote.post_id == alias_post.id, isouter=True).group_by(alias_post.id).order_by(alias_post.updated_at.desc()).limit(limit).all()
    
    return posts

@router.get("/{id}", response_model=PostVoteReponse)
def get_post(id: int, db: Session = Depends(get_db), 
             current_user: dict = Depends(get_current_user)):
    
    # post = db.get(Post,id)
    alias_post = aliased(Post, name='post')
    post_result = db.query(alias_post, func.count(Vote.post_id).label("votes")).join(Vote,Vote.post_id == alias_post.id, isouter=True).filter(alias_post.id == id).group_by(alias_post.id).first()
    
    if not post_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"posts with id {id} not found!")
    
    if post_result.post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to perform requested action")
        
    return post_result

@router.get("/users/{user_id}", response_model=List[PostVoteReponse])
def get_user_posts(user_id: int, db: Session = Depends(get_db), 
             current_user: dict = Depends(get_current_user)):
    
    # post = db.get(Post,id)
    alias_post = aliased(Post, name='post')
    posts = db.query(alias_post, func.count(Vote.post_id).label("votes")).join(Vote,Vote.post_id == alias_post.id, isouter=True).filter(alias_post.owner_id == user_id).group_by(alias_post.id).all()
    
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"posts created with user id {user_id} not found!")
    
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to perform requested action")
        
    return posts

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