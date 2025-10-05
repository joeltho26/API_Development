from fastapi import status, HTTPException, Depends, Response, APIRouter
from ..schemas.vote import VoteBase, VoteResponse
from ..models.vote import Vote
from ..models.post import Post
from ..database import get_db
from sqlalchemy.orm import Session
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/vote",
    tags=['Votes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: VoteBase, db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    
    post = db.query(Post).filter(Post.id == vote.post_id).first()
    if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"post with post id {vote.post_id} is not found!")
    
    #vote_query = db.query(Vote).filter(Vote.post_id==vote.post_id).filter(Vote.user_id==current_user.id)
    vote_query = db.query(Vote).filter(Vote.post_id==vote.post_id, Vote.user_id==current_user.id)
    vote_found = vote_query.first()
    if vote.dir == 1:
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                        detail=f"user: {current_user.id} already liked the post {vote.post_id}!")
        
        new_vote = Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote!"}
    else:
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"user: {current_user.id} has not liked the post yet! {vote.post_id}!")
            
        vote_query.delete(sychronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote!"}