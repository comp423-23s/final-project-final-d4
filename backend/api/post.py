from fastapi import APIRouter, Depends, HTTPException
from ..services.post import PostService
from ..models.post import Post

openapi_tags = {"name": "Post view", "description": "Post projects endpoints."}

api = APIRouter(prefix="/api/post")

@api.get("", tags=["Post view"])
def get_posts(post_serv: PostService = Depends()) -> list[Post]:
    return post_serv.get()

@api.post("", tags=["Post view"])
def create_post(post: Post, post_serv: PostService = Depends()) -> Post:
    try:
        return post_serv.create_post(post)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))