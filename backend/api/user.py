from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..services import UserService
from ..models import User
from .authentication import registered_user

api = APIRouter(prefix="/api/user")


@api.get("", response_model=list[User], tags=['User'])
def search(q: str, subject: User = Depends(registered_user), user_svc: UserService = Depends()):
    return user_svc.search(subject, q)

@api.get("/{pid}", response_model=User, tags=['User'])
def get_byPID(pid: int, user_svc: UserService = Depends()):
    try:
        return user_svc.get(pid)
    except Exception as e:
            raise HTTPException(status_code=422, detail=str(e))