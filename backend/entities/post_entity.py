'''Posts for all registered users in the application.'''


from sqlalchemy import Integer, String, DateTime, ARRAY, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.mutable import MutableList
from typing import Self
from datetime import datetime
from .entity_base import EntityBase
from ..models import Post


# __authors__ = ['Chalisa Phoomsakha']
# __copyright__ = 'Copyright 2023'
# __license__ = 'MIT'


class PostEntity(EntityBase):
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String(64), unique=True, index=True, default='')
    tags: Mapped[list[str]] = mapped_column(MutableList.as_mutable(ARRAY(String(64))))
    created: Mapped[datetime] = mapped_column(DateTime)
    
    user_id = mapped_column(ForeignKey("users.PID"))
    postedBy: Mapped[list['UserEntity']] = relationship(back_populates="userPosts", post_update=True)

    comments: Mapped['CommentEntity'] = relationship(back_populates='post')

    @classmethod
    def from_model(cls, model: Post) -> Self:
        return cls(
            id=model.id,
            content=model.content,
            tags=model.tags,
            created=model.created,
            postedBy=model.postedBy,
            comments=model.comments,
        )

    def to_model(self) -> Post:
        return Post(
            id=self.id,
            content=self.content,
            tags=self.tags,
            created=self.created,
            postedBy=self.postedBy,
            comments=self.comments,
        )

    # not sure if necessary
    # def update(self, model: Post) -> None:
    #     self.content = model.content
    #     self.tags = model.tagss