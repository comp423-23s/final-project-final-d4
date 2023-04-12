from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import db_session
from ..models import Comment
from ..entities import PostEntity, CommentEntity, UserEntity

# #: Comments
# class Comment(BaseModel):
#     id: int | None = None
#     commenter: int | None
#     post: int
#     replies: list['Comment'] = []
#     text: str = ""
#     created: datetime = datetime.now()
#     # class Config:
#     #     orm_mode = True

class CommentService:

    _session: Session

    def __init__(self, session: Session = Depends(db_session)):
        self._session = session

    def all(self) -> list[Comment]:
        query = select(CommentEntity)
        entities = self._session.scalars(query).all()
        return [entity.to_model() for entity in entities]
    
    def create(self, comment: Comment) -> Comment:
        user = self._session.get(UserEntity, comment.commenter)
        if user:
            comment.commenter = user
            post = self._session.get(PostEntity, comment.post)
            comment.post = post
            comment_entity: CommentEntity = CommentEntity.from_model(comment)
            post.comments.append(comment_entity)
            self._session.add(comment_entity)
            self._session.commit()
            return comment_entity.to_model()
        else:
            raise ValueError(f"No user found with PID: {comment.commenter}")
            
    def get(self, id: int) -> Comment | None:
        post = self._session.get(CommentEntity, id)
        if post:
            return post.to_model()
        else:
            raise ValueError(f"Comment not found")

    def delete(self, id: int) -> None:
        comment = self._session.get(CommentEntity, id)
        if comment:
            post = self._session.get(PostEntity, comment.post.id)
            post.comments.remove(comment)
            self._session.delete(comment)
            self._session.commit()
            return None
        else:
            raise ValueError(f"No post found")
        
    def update(self, comment_id: int, newText: str) -> Comment:
        temp = self._session.get(CommentEntity, comment_id)
        if temp:
            temp.text = newText
            self._session.commit()
            return temp.to_model()
        else:
            raise ValueError(f"Comment not found")

    def reply(self, comment_id: int, reply: Comment) -> Comment:
        temp = self._session.get(CommentEntity, comment_id)
        if temp:
            reply = self._session.get(CommentEntity, reply.id)
            reply.replyTo_id = temp.id
            temp.replies.append(reply)
            self._session.add(reply)
            self._session.commit()
            return temp.to_model()
        else:
            raise ValueError(f"Comment not found")