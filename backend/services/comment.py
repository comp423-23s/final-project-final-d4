"""This file provide services for comment application.

This file includes basic features a comment should have, which are get comments: all(),
create comments: create(), and delete comments: delete(). We include a feature of private
comments, which is only visible among the author of the post, the author of the comment, 
and the administrator. And only the author of the comment of the administrator are able 
to delete the comment.
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import Comment,User
from ..models.comment import NewComment
from ..entities import PostEntity, CommentEntity, UserEntity
from .permission import PermissionService, UserPermissionError

class CommentService:
    """This class defines operations towards comments.

    This class contains basic operations towards comments, including get comments,
    create comments, and delete comments

    Attributes:
        _session: A Session helping connect the ORM
        _permission: A PermissionService helping check user permission
    """

    _session: Session
    _permission: PermissionService

    def __init__(self, session: Session = Depends(db_session), permission: PermissionService=Depends()):
        """Initializes the instance based on session and permission.

        Args:
          session: Defines which session it uses.
          permission: Defines which permissionservice it uses
        """
        self._session = session
        self._permission = PermissionService(session)

    def all(self,subject:User,post_id:int) -> list[Comment]:
        """Fetch all comments from a post visible to the user.

        Retrieves comments from the post pertaining to the given post id. 
        Comments are visible to the user if the user is admin, author of 
        post, or the author of the comment.

        Args:
            subject: An object of User representing the current user
            post_id: An Integer representing which post is the user extracting comments from

        Returns:
            A list of object Comment that is visible to the current user.

        Raises:
            ValueError: An error occurred accessing the post if the post does not exist.
        """
        post_query = select(PostEntity).where(PostEntity.id == post_id)
        post_entity: PostEntity = self._session.scalar(post_query)
        if (post_entity is None):
            raise ValueError(f"Post with id {post_id} does not exist")
        if self._permission.check(subject,"admin*","*"):
            query = select(CommentEntity).join(PostEntity).where(
                PostEntity.id == post_id)
        else:
            query = select(CommentEntity).join(PostEntity).where(
            (PostEntity.id == post_id) &
            (
                ~CommentEntity.private |
                (
                    CommentEntity.private & (
                        (PostEntity.user_pid == subject.pid) |
                        (CommentEntity.user_id == subject.pid)
                    )
                )
            )
        )
        entities = self._session.execute(query).scalars().all()
        return [entity.to_model() for entity in entities]
    
    def create(self, user: User, comment: NewComment, post_id: int) -> Comment:
        """Create a comment under a post.

        Given necessary information about what the current user wants to post,
        put the information into the database

        Args:
            user: An object of User representing the current user
            comment: An object of NewComment recording the information such as title and contents about what the user wants to comment

        Returns:
            An object of Comment that is transferred to the database.

        Raises:
            ValueError: An error occurred accessing the user if the user does not exist.
            ValueError: An error occurred accessing the post if the post does not exist.
        """
        query = select(UserEntity).where(UserEntity.pid == user.pid)
        user_entity: UserEntity = self._session.scalar(query)
        if (user_entity is None):
            raise ValueError("User not registered")
        
        post_query = select(PostEntity).where(PostEntity.id == post_id)
        post_entity: PostEntity = self._session.scalar(post_query)
        if (post_entity is None):
            raise ValueError(f"Post with id {post_id} does not exist")
    
        comment_model = Comment(
            commenter = user.pid,
            post = post_id,
            text = comment.text,
            created= comment.created,
            private = comment.private
        )
        
        comment_entity: CommentEntity = CommentEntity.from_model(comment_model)        
        self._session.add(comment_entity)
        self._session.flush()
        self._session.commit()
        return comment_entity.to_model()
            
    def delete(self, subject: User, post_id: int, comment_id:int) -> None:
        """Delete a comment under a post.

        Deletes comments from the post pertaining to the given post id. 
        Only the admin and the author of the comment can delet the comment.

        Args:
            subject: An object of User representing the current user
            post_id: An Integer representing which post the user is deleting comments from
            comment_id: An Integer representing which comment the user is deleting

        Returns:
            None

        Raises:
            ValueError: An error occurred accessing the comment if the user does not exist.
            UserPermissionError: An error occurred if the user is not allowed to delete the comment.
        """
        for i in self.all(subject,post_id):
            if i.id == comment_id:
                comment_entity = self._session.query(CommentEntity).filter(CommentEntity.id == comment_id).one()
                if comment_entity is None:
                    raise ValueError("The comment is not in the system.")
                else:
                    user_pid = comment_entity.to_model().commenter
                    query = select(UserEntity).where(UserEntity.pid == user_pid)
                    user_entity: UserEntity = self._session.scalar(query)
                    user = user_entity.to_model()
                    if subject != user:
                        self._permission.enforce(subject, "comment.delete", f"comment/{comment_id}")
    
                    self._session.delete(comment_entity)
                    self._session.commit()
                return comment_entity.to_model()