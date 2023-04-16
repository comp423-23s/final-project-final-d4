from fastapi import Depends
from sqlalchemy import select, or_, func
from sqlalchemy.orm import Session
from ..database import db_session
from .permission import PermissionService, UserPermissionError
from ..models import Post, User, permission
from ..models.post import NewPost
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
            PostEntity.description.ilike(f'%{query}%'),
        )
        statement = statement.where(criteria).limit(10)
        entities = self._session.execute(statement).scalars()
        return [entity.to_model() for entity in entities]
    
    # Create new post
    def create_post(self, post: NewPost, user: User) -> Post | None:
        query = select(UserEntity).where(UserEntity.pid == user.pid)
        user_entity: UserEntity = self._session.scalar(query)
        if (user_entity is None):
            raise ValueError("User not registered")
        
        post_model = Post(
            content=post.content,
            tags = post.tags,
            created=post.created,
            title = post.title,
            description=post.description
        )
        
        post_entity = PostEntity.from_model(post_model)
        post_entity.postedBy = user_entity
        self._session.add(post_entity)
        self._session.flush()
        self._session.commit()
        return post_entity.to_model()
    
    # Delete post
    def delete_post(self, subject: User, id: int) -> Post | None:
        """

        """
        # Get post user entity from post id
        post_entity = self._session.query(PostEntity).filter(PostEntity.id == id).one()
        if post_entity is None:
            raise ValueError("The post is not in the system.")
        else:
            user_pid = post_entity.to_model().pid
            query = select(UserEntity).where(UserEntity.pid == user_pid)
            user_entity: UserEntity = self._session.scalar(query)
            user = user_entity.to_model()
            if subject.pid != user.pid:
                self._permission.enforce(subject, 'post.delete', f'post/{id}')
            self._session.delete(post_entity)
            self._session.commit()
            return post_entity.to_model()