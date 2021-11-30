from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm.session import Session
from ..database import get_db
from typing import Optional, List
from starlette.responses import Response
from sqlalchemy import func
router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model= List[schemas.Post])
def get_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
limit:Optional[int] = 5, skip:int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * from posts """)
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts =  db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)

    return posts
    

@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def create_post(data: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) 
    # VALUES (%s, %s, %s) RETURNING * """, (data.title, data.content, data.published))
    
    # new_post = cursor.fetchone()

    # conn.commit() #save changes
    
    new_post = models.Post(user_id = current_user.id, **data.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model= schemas.Post)
def get_post(id: int,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id),))
    # data = cursor.fetchone()
    data =  db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not data:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND
        , detail= f"no post with id: {id}")
    return data

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s""", (str(id),))
    # deleted_post = cursor.fetchone()
    posts = db.query(models.Post).filter(models.Post.id == id)
    
    if posts.first() == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND
        , detail= "that post not exists")
    if posts.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        detail= "Not Allowed to perform action")
        # conn.commit()
    posts.delete(synchronize_session=False)
    db.commit()
    return Response(status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model= schemas.PostResponse)
def update_post(id: int, data: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s
    # WHERE id = %s RETURNING * """,(data.title, data.content, data.published, str(id)))

    # updated_post = cursor.fetchone()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post =  post_query.first()

    if post_query == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND
        , detail= f"no post with id: {id}")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        detail= "Not Allowed to perform action")
        # conn.commit()
    post_query.update(data.dict(), synchronize_session=False)
    db.commit()
       
    return post_query.first()