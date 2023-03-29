from fastapi import APIRouter, Depends
from ..services.post import PostService
from ..models.post import Post

openapi_tags = {"name": "Post view", "description": "Post projects endpoints."}

api = APIRouter(prefix="/api/post")

@api.get("", tag=["Post view"])
def get_posts(post_serv: PostService = Depends()) -> list[Post]:
    return post_serv.get()

@api.post("", tag=["Post view"])
def create_post(post: Post, post_serv: PostService = Depends()) -> Post:
    return post_serv.create(post)