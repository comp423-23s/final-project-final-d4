from fastapi import APIRouter, Depends, HTTPException
from ..services.post import PostService
from ..models.post import Post
from ..models import User
from .authentication import registered_user

openapi_tags = {"name": "Post view", "description": "Post projects endpoints."}

api = APIRouter(prefix="/api/post")

@api.get("", tags=["Post view"])
def get_posts(post_serv: PostService = Depends()) -> list[Post]:
    return post_serv.get_posts()

@api.get("/{search_string}", response_model=list[Post], tags=["Search post"])
def search_post(search_string: str, post_serv: PostService = Depends()) -> list[Post]:
    try:
        return post_serv.search_post(search_string)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@api.post("", tags=["Post view"])
def create_post(post: Post, post_serv: PostService = Depends(), subject: User = Depends(registered_user)) -> Post:
    try:
        return post_serv.create_post(post, subject)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@api.delete("/{id}",tags=["Post"])
def delete_post(id:int, post_serv: PostService = Depends(), subject: User = Depends(registered_user)) -> Post:
    try:
        return post_serv.delete_post(id,subject)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))