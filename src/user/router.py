from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import session, crud
from src.user.schemas import UserIn, UserOut

router = APIRouter(
    prefix="/users"
)


@router.post("", response_model=UserOut)
def post_user(
        db: Annotated[Session, Depends(session.get_db)],
        post_user_request: UserIn
):
    user = crud.create_user(db, post_user_request)
    return user


@router.get("/{user_id}", response_model=UserOut)
def get_user(
        db: Annotated[Session, Depends(session.get_db)],
        user_id: int
):
    user = crud.read_user(db, user_id=user_id)
    return user
