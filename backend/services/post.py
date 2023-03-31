from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import select, or_, func
from sqlalchemy.orm import Session
from ..database import db_session
from .permission import PermissionService
from ..models import Post
from ..entities.post_entity import PostEntity
from ..entities import UserEntity



# class Post_raw(BaseModel):
#     postedBy : int
#     title : str = ""
#     description: str = ""
#     content: str = ""
#     dateTime: datetime = datetime.now()
#     tag: list[str] = []
#     comment : list[comment] = []


class PostService:

    _session: Session
    _permission: PermissionService

    def __init__(self, session: Session = Depends(db_session), permission: PermissionService = Depends()):
        self._session = session
        self._permission = permission

    # Get all posts
    def get_posts(self) -> list[Post] | None:
        query = select(PostEntity)
        entities = self._session.scalar(query).all()
        return [entity.to_model() for entity in entities]
        
    # Create new post
    def create_post(self, post: Post) -> Post | None:
        stmt = select(UserEntity).where(UserEntity.pid == post.postedBy)
        user_entity = self._session.scalar(stmt).one_or_none()

        if user_entity:
            post.postedby = user_entity.id
        else:
            raise Exception("User not found")
    
        post_entity = PostEntity.from_model(post)
        self._session.add(post_entity)
        self._session.flush()
        self._session.commit()
        return post_entity.to_model()