from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import Comment,User
from ..models.comment import NewComment
from ..entities import PostEntity, CommentEntity, UserEntity
from .permission import PermissionService, UserPermissionError

class CommentService:

    _session: Session
    _permission: PermissionService

    def __init__(self, session: Session = Depends(db_session), permission: PermissionService=Depends()):
        self._session = session
        self._permission = PermissionService(session)

    # get comments given a post id and current user
    def all(self,subject:User,post_id:int) -> list[Comment]:
        # Given a post id and the curren user, this would return a list of Comment that is visible to the user"
        post_query = select(PostEntity).where(PostEntity.id == post_id)
        post_entity: PostEntity = self._session.scalar(post_query)
        if (post_entity is None):
            raise ValueError(f"Post with id {post_id} does not exist")
        admin = self._permission._has_permission(subject.permissions,"admin*","*")
        if admin:
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
    
    # create a comment to a post
    def create(self, user: User, comment: NewComment) -> Comment:
        query = select(UserEntity).where(UserEntity.pid == user.pid)
        user_entity: UserEntity = self._session.scalar(query)
        if (user_entity is None):
            raise ValueError("User not registered")
        
        post_query = select(PostEntity).where(PostEntity.id == comment.post)
        post_entity: PostEntity = self._session.scalar(post_query)
        if (post_entity is None):
            raise ValueError(f"Post with id {comment.post} does not exist")
    
        comment_model = Comment(
            commenter = user.pid,
            post = comment.post,
            text = comment.text,
            created= comment.created,
            private = comment.private
        )
        
        comment_entity: CommentEntity = CommentEntity.from_model(comment_model)        
        self._session.add(comment_entity)
        self._session.flush()
        self._session.commit()
        return comment_entity.to_model()
            
    # delete a comment
    def delete(self, subject: User, post_id: int, comment_id:int) -> None:
        # user.permissions = self._permission.get_permissions(user)
        # admin = self._permission.enforce(user,"comment.delete","*")
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
            
        
    # def update(self, comment_id: int, newText: str) -> Comment:
    #     temp = self._session.get(CommentEntity, comment_id)
    #     if temp:
    #         temp.text = newText
    #         self._session.commit()
    #         return temp.to_model()
    #     else:
    #         raise ValueError(f"Comment not found")

    # def reply(self, comment_id: int, reply: Comment) -> Comment:
    #     temp = self._session.get(CommentEntity, comment_id)
    #     if temp:
    #         reply = self._session.get(CommentEntity, reply.id)
    #         reply.replyTo_id = temp.id
    #         temp.replies.append(reply)
    #         self._session.add(reply)
    #         self._session.commit()
    #         return temp.to_model()
    #     else:
    #         raise ValueError(f"Comment not found")
        
    # def search(self, id: int) -> Comment | None:
    #     post = self._session.get(CommentEntity, id)
    #     if post:
    #         return post.to_model()
    #     else:
    #         raise ValueError(f"Comment not found")
