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
    content: Mapped[str] = mapped_column(String(64), unique=False, index=True, default='')
    tags: Mapped[list[str]] = mapped_column(MutableList.as_mutable(ARRAY(String(64))))
    created: Mapped[datetime] = mapped_column(DateTime)
    title: Mapped[str] = mapped_column(String(64), unique=False, index=True, default='')
    description: Mapped[str] = mapped_column(String(64), unique=False, index=True, default='')
    
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=True)
    postedBy: Mapped['UserEntity'] = relationship(back_populates="userPosts", post_update=True)
    # comments: Mapped[list['CommentEntity']] = relationship(back_populates='post')

    @classmethod
    def from_model(cls, model: Post) -> Self:
        return cls(
            id=model.id,
            content=model.content,
            tags=model.tags,
            created=model.created,
            title = model.title,
            description = model.description
        )

    def to_model(self) -> Post:
        return Post(
            id=self.id,
            content=self.content,
            tags=self.tags,
            created=self.created,
            title = self.title,
            description = self.description
        )

    # not sure if necessary
    # def update(self, model: Post) -> None:
    #     self.content = model.content
    #     self.tags = model.tagss