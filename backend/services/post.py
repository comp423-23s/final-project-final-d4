from fastapi import Depends
from sqlalchemy import select, or_, func
from sqlalchemy.orm import Session
from ..database import db_session
from .permission import PermissionService
from ..models.post import Post
from ..entities.post_entity import PostEntity


class PostService:

    _session: Session
    _permission: PermissionService

    def __init__(self, session: Session = Depends(db_session), permission: PermissionService = Depends()):
        self._session = session
        self._permission = permission

    # Get all posts
    def get(self) -> list[Post] | None:
        return

    # Create new post
    def create(self, post: Post) -> Post | None:
        post_entity = PostEntity.from_model(post)
        self._session.add(post_entity)
        self._session.flush()
        self._session.commit()
        return post_entity.to_model()
