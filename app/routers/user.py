from sqlalchemy.sql.functions import user
from .. import models, schemas, utils
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm.session import Session
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.UserResponse)
def create_users(data: schemas.UserCreate, db: Session = Depends(get_db)):
    #hashing password
    
    data.password = utils.hash(data.password)
    new_user = models.User(**data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail= f"no user with id {id}")

    return user