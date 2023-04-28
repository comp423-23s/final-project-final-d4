'''Comments for all registered users in the application.'''


from sqlalchemy import Boolean, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self
from datetime import datetime
from .entity_base import EntityBase
from ..models import Comment

class CommentEntity(EntityBase):
    __tablename__ = 'comment'

    id : Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id = mapped_column(ForeignKey("user.pid"))
    commenter: Mapped['UserEntity'] = relationship(post_update=True)

    post_id = mapped_column(ForeignKey("post.id"))
    post: Mapped['PostEntity'] = relationship(back_populates="comments", post_update=True)

    private : Mapped[bool] = mapped_column(Boolean)

    text: Mapped[str] = mapped_column(String(64))
    created: Mapped[datetime] = mapped_column(DateTime)

    @classmethod
    def from_model(cls, model: Comment) -> Self:
        return cls(
            id=model.id,
            text=model.text,
            created=model.created,
            user_id=model.commenter,
            post_id=model.post,
            private = model.private
        )

    def to_model(self) -> Comment:
        return Comment(
            id=self.id,
            text=self.text,
            commenter=self.user_id,
            created=self.created,
            post=self.post_id,
            private=self.private
        )