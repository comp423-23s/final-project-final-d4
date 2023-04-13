from fastapi import Depends
from sqlalchemy import select, or_, func
from sqlalchemy.orm import Session
from ..database import db_session
from .permission import PermissionService, UserPermissionError
from ..models import Post,User,Permission
from ..entities.post_entity import PostEntity
from ..entities import UserEntity

class PostService:
    _session: Session
    _permission: PermissionService

    def __init__(self, session: Session = Depends(db_session), permission: PermissionService=Depends()):
        self._session = session
        self._permission = PermissionService(session)

    # Get all posts
    def get_posts(self) -> list[Post] | None:
        query = self._session.query(PostEntity)
        entities = query.all()
        return [entity.to_model() for entity in entities]

    # Search posts
    def search_post(self, query: str) -> list[Post] | None:        
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
        query = select(UserEntity).where(UserEntity.pid == user.pid)
        user_entity: UserEntity = self._session.scalar(query)
        post_entity = PostEntity.from_model(post)
        post_entity.postedBy = user_entity
        self._session.add(post_entity)
        self._session.flush()
        self._session.commit()
        return post_entity.to_model()
    
    # Delete post
    def delete_post(self, id: int, subject: User) -> Post | None:
        subject.permissions = self._permission.get_permissions(subject)
        admin = self._permission._has_permission(subject.permissions,"admin.*","*")
        for i in self.get_posts():
            if i.id == id:
                post_entity = self._session.query(PostEntity).filter(PostEntity.id == id).one()
                if post_entity is None:
                    raise ValueError("The post is not in the system.")
                else:
                    if((post_entity.postedBy == subject.pid) | admin):
                        # Check for authorization
                        self._session.delete(post_entity)
                        self._session.commit()
                    else:
                        raise UserPermissionError('post.delete_post', f'post/{id}')
           
                return post_entity

                

        
    
    
