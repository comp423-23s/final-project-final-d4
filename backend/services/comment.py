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

    # get comments given a post id
    def all(self,post_id:int) -> list[Comment]:
        post_query = select(PostEntity).where(PostEntity.id == post_id)
        post_entity: PostEntity = self._session.scalar(post_query)
        if (post_entity is None):
            raise ValueError(f"Post with id {post_id} does not exist")
        
        query = select(CommentEntity).join(PostEntity).where(PostEntity.id == post_id)
        entities = self._session.execute(query).scalars().all()
        return [entity.to_model() for entity in entities]
    
    # create a comment to a post
    def create(self, comment: NewComment, user: User) -> Comment:
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
            created= comment.created
        )
        
        comment_entity: CommentEntity = CommentEntity.from_model(comment_model)        
        self._session.add(comment_entity)
        self._session.flush()
        self._session.commit()
        return comment_entity.to_model()
            
    # delete a comment
    def delete(self, post_id: int, comment_id:int, user: User) -> None:
        user.permissions = self._permission.get_permissions(user)
        admin = self._permission._has_permission(user.permissions,"admin.*","*")
        for i in self.all(post_id):
            if i.id == comment_id:
                comment_entity = self._session.query(CommentEntity).filter(CommentEntity.id == comment_id).one()
                if comment_entity is None:
                    raise ValueError("The comment is not in the system.")
                else:
                    print(comment_entity.commenter)
                    if((i.commenter == user.pid) | admin):
                        # Check for authorization
                        self._session.delete(comment_entity)
                        self._session.commit()
                    else:
                        raise UserPermissionError('comment.delete_comment', f'comment/{comment_id}')
           
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
