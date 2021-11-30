from typing import Optional
from pydantic import BaseModel 
from datetime import datetime
from pydantic.errors import ClassError

from pydantic.networks import EmailStr
from pydantic.types import conint
from sqlalchemy.sql.functions import user
from sqlalchemy.sql.sqltypes import TIMESTAMP
#the schema is for verifying the body request and response, where the model is to match with the DB

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_time: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    

class PostCreate(PostBase):
    pass 

class PostResponse(PostBase):
    id: int
    created_time: datetime
    user_id: int
    user: UserResponse
    #the 3 other properties already inheritted

    class Config:
        orm_mode = True

class Post(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    tken_type: str

class TokenData(BaseModel):
    id: Optional[str]= None

class Vote(BaseModel):
    post_id:int
    dir: conint(le=1)
