from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import select, or_, func
from sqlalchemy.orm import Session
from ..database import db_session, _engine_str
from .permission import PermissionService, UserPermissionError
from ..models import Post,User,Permission
from ..entities.post_entity import PostEntity
from ..entities import UserEntity
from sqlalchemy import create_engine


class PostService:
    _session: Session
    _permission: PermissionService

    def __init__(self, session: Session = Depends(db_session), permission: PermissionService = Depends()):
        self._session = session
        self._permission = permission

    @staticmethod
    def create_session() -> Session:
        engine = create_engine(_engine_str())
        return Session(bind=engine)

    # Get all posts
    def get_posts(self) -> list[Post] | None:
        # if session is None:
        #     session = self.create_session()
        query = self._session.query(PostEntity)
        entities = query.all()
        return [entity.to_model() for entity in entities]

    # Search posts
    def search_post(self, query: str) -> list[Post] | None:
        # if session is None:
        #     session = self.create_session()
        
        statement = select(PostEntity)
        criteria = or_(
            PostEntity.content.ilike(f'%{query}%'),
            PostEntity.title.ilike(f'%{query}%'),
            UserEntity.description.ilike(f'%{query}%'),
        )
        statement = statement.where(criteria).limit(10)
        entities = self._session.execute(statement).scalars()
        return [entity.to_model() for entity in entities]
    
    # Create new post
    def create_post(self, post: Post, user: User) -> Post | None:
        # if session is None:
        #     session = self.create_session()
        
        query = select(UserEntity).where(UserEntity.pid == user.pid)
        user_entity: UserEntity = self._session.scalar(query)
        post_entity = PostEntity.from_model(post)
        post_entity.postedBy = user_entity
        self._session.add(post_entity)
        self._session.flush()
        self._session.commit()
        return post_entity.to_model()
    
    # Delete post
    def delete_post(self, id: int, subject: User, session: Session=None) -> Post | None:
        if session is None:
            session = self.create_session()
        admin = False
        perm = self._permission.get_permissions(subject)
        if(Permission(action="admin.*", resource="*") in perm):
            admin=True

        for i in self.get_posts():
            if i.id == id:
                post_entity = session.query(PostEntity).filter(PostEntity.id == id).one()
                if((post_entity.postedBy == subject.pid) | admin):
                    session.delete(post_entity)
                    session.commit()
                else:
                    raise UserPermissionError('post.delete_post', f'post/{id}')
           
                return post_entity

        
    
    
