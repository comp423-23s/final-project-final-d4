from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import select, or_, func
from sqlalchemy.orm import Session
from ..database import db_session, _engine_str
from .permission import PermissionService
from ..models import Post
from ..entities.post_entity import PostEntity
from ..entities import UserEntity
from sqlalchemy import create_engine


# class Post_raw(BaseModel):
#     postedBy : int
#     title : str = ""
#     description: str = ""
#     content: str = ""
#     dateTime: datetime = datetime.now()
#     tag: list[str] = []
#     comment : list[comment] = []


class PostService:
    # _session: Session
    _permission: PermissionService

    def __init__(self, session: Session = Depends(db_session), permission: PermissionService = Depends()):
        # self._session = session
        self._permission = permission

    @staticmethod
    def create_session() -> Session:
        engine = create_engine(_engine_str())
        return Session(bind=engine)

    # Get all posts
    def get_posts(self, session: Session = None) -> list[Post] | None:
        if session is None:
            session = self.create_session()
        query = session.query(PostEntity)
        entities = query.all()
        return [entity.to_model() for entity in entities]
        
    # Create new post
    def create_post(self, post: Post, session: Session = None) -> Post | None:
        if session is None:
            session = self.create_session()
        
        if (len(str(post.postedBy)) != 9):
            raise Exception(f"Invalid PID: {post.postedBy}")
        
        stmt = select(UserEntity).join(UserEntity.userPosts).where(UserEntity.pid == post.postedBy)
        user = session.scalars(stmt).one_or_none()
        if user is None:
            raise Exception(f"User with PID: {post.postedBy} not existed")
    
        post_entity = PostEntity.from_model(post)
        self._session.add(post_entity)
        self._session.flush()
        self._session.commit()
        return post_entity.to_model()
    
    # Delete post
    def delete_post(self, id: int, session: Session=None) -> Post | None:
        if session is None:
            session = self.create_session()

        for i in self.get_posts():
            if i.id == id:
                post_entity = session.query(PostEntity).filter(PostEntity.id == id).one()
                session.delete(post_entity)
                session.commit()
                return post_entity
        
        raise ValueError("The user is not in the system.")
    
    
