from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..services import UserService
from ..models import User
from .authentication import registered_user

api = APIRouter(prefix="/api/user")

# class Post(BaseModel):
#     id: int
#     title: str
#     description: str
#     content: str
#     dateTime: str
#     tag: list[str]


@api.get("", response_model=list[User], tags=['User'])
def search(q: str, subject: User = Depends(registered_user), user_svc: UserService = Depends()):
    return user_svc.search(subject, q)
