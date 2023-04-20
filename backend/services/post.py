""" This file provides the service for post. It contains the following functions:

This file includes basic features relating to post including get all posts in the database, searching for posts that
has content, description, title that match with the search string, creating a post, and deleting a post. The delete_post
function is only available to the author of the post and the administrator.
"""

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
    """This class defines operations towards posts.
    
    This class contains basic operations towards posts, including get posts, search posts, 
    create posts, and delete posts.

    Attributes:
        _session: A Session helping connect the ORM
        _permission: A PermissionService helping check user permission
    """
    _session: Session
    _permission: PermissionService

    def __init__(self, session: Session = Depends(db_session), permission: PermissionService=Depends()):
        self._session = session
        self._permission = permission

    # Get all posts
    def get_posts(self) -> list[Post] | None:
        """Get all posts in the database.

        Retrieve all posts in the post table in the database.

        Returns:
            A list of Post object that contains all posts in the database.
        """
        query = self._session.query(PostEntity)
        entities = query.all()
        return [entity.to_model() for entity in entities]

    # Search posts
    def search_post(self, query: str) -> list[Post] | None:
        """ Search for posts

        Retrieve all posts that has content, description, title that match with the search string.
        
        Args:
            query: A string that is used to search for posts that has content, description, title that match
            with the search string.
            
        Returns:
            A list of Post object that contains all posts that has content, description, title that match
            with the search string.
            Return None if no posts are found.
        """        
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
        """Create a new post.

        Given a NewPost object, create a new post in the database.

        Args:
            post: A NewPost object that contains the content, tags, created, title, and description of the post.
            user: A User object that contains the pid of the user who created the post. The user object is dependent
            on the registered_user function in the authentication.py file.
        
        Returns:
            A Post object that contains post id, content, tags, created time, title, description, and pid of the user
            who created the post.

        Raises:
            ValueError: If the user is not registered in the database.
        """
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
        """Delete a post.

        Given a post id, delete the post from the database. The post can only be deleted by the author of the post
        or the administrator.

        Args:
            subject: A User object that contains the pid of the user who wants to delete the post. The user object is
            dependent on the registered_user function in the authentication.py file.
            id: An integer that is the id of the post that the user wants to delete.
        
        Returns:
            The deleted Post object.
            Return None if the post is not in the database.
        
        Raises:
            ValueError: If the post associated with the id is not in the database.
            UserPermissionError: If the user is not the author of the post and is not an administrator.
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
        
    # update post
    def update(self, subject: User,
                id: int, 
                content: str | None,
                title: str | None, 
                description: str | None, 
                tags: list[str] | None,) -> Post:
        """Update a post.

        Given a post id, update the post in the database. 
        TODO: The post can only be updated by the author of the post or the administrator.

        Args:
            id: An integer that is the id of the post that the user wants to delete.
            content: An optional string that is the new content for the post that the user wants to update
            title: An optional string that is the new title for the post that the user wants to update
            description: An optional string that is the new description for the post that the user wants to update
            tags:  An optional lit of strings that is the new tags for the post that the user wants to update
        
        Returns:
            The updated Post object.
            Throws error if the post is not in the database.
        
        Raises:
            ValueError: If the post associated with the id is not in the database.
        """
        temp = self._session.get(PostEntity, id)
        if temp:
            user_pid = temp.to_model().pid
            query = select(UserEntity).where(UserEntity.pid == user_pid)
            user_entity: UserEntity = self._session.scalar(query)
            user = user_entity.to_model()
            if subject.pid != user.pid:
                self._permission.enforce(subject, 'post.update', f'post/{id}')

            if content != None:
                temp.content = content
            if title != None:
                temp.title = title
            if description != None:
                temp.description = description
            if tags != None:
                temp.tags = tags
            self._session.commit()
            return temp.to_model()
        else:
            raise ValueError("The post is not in the system.") 