# from typing import Optional, List
from fastapi import FastAPI, status, HTTPException
# from fastapi.params import Body, Depends
# from passlib.utils.decor import deprecated_function
# from pydantic import BaseModel
# from sqlalchemy.orm.session import Session
# from sqlalchemy.sql.expression import insert
# from sqlalchemy.sql.functions import user
# from starlette.responses import Response
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# while True:

#     try:
#         conn = psycopg2.connect(host = 'localhost', database= 'fastapi',
#         user='postgres', password='W1ld4nadli', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("DBConnected!")
#         break
#     except Exception as error:
#         print("Error: ", error)
#         time.sleep(3)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Welcome!!"}



