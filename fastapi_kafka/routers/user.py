from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fastapi_kafka.schemas import UserCreate, User
from fastapi_kafka.database import get_db
from fastapi_kafka import crud
from fastapi_kafka.jwt_auth import get_current_active_user

routes = APIRouter(
    prefix="/user",
    tags=['user'],
    responses={404: {"description": "Not Found"}}
)


@routes.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registred")

    return crud.create_user(db=db, user=user)


@routes.get("/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users


@routes.get("/me", response_model=User)
async def read_user_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@routes.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user
