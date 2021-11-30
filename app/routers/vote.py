from sqlalchemy.sql.functions import mode
from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm.session import Session
from ..database import get_db
from typing import Optional, List
from starlette.responses import Response

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {vote.post_id} not exists")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id
         == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()     
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already vote on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return{"message":"successfully vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="votes doesnot exists")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return{"message":"success delete vote"}
        