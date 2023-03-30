from fastapi import Depends
from sqlalchemy import select, or_, func
from sqlalchemy.orm import Session
from ..database import db_session
from .permission import PermissionService
from ..models import post
from ..entities.post_entity import PostEntity

class PostService:

    _session: Session
    _permission: PermissionService

    def __init__(self, session: Session = Depends(db_session), permission: PermissionService = Depends()):
        self._session = session
        self._permission = permission


    def get_posts() -> list[post]:
        query = select(PostEntity)
        entities= self._session.scalars(query).all()
        return [entity.to_model() for entity in entities]


    # def create() -> Post | None:

    