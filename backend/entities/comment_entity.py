'''Comments for all registered users in the application.'''


from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
# from sqlalchemy.ext.mutable import MutableList
from typing import Self
from datetime import datetime
from .entity_base import EntityBase
from .reply_entity import reply_table
from ..models import Comment


# __authors__ = ['Chalisa Phoomsakha']
# __copyright__ = 'Copyright 2023'
# __license__ = 'MIT'


class CommentEntity(EntityBase):
    __tablename__ = 'comment'

    id = mapped_column(Integer, primary_key=True)

    user_id = mapped_column(ForeignKey("user.pid"))
    commenter: Mapped['UserEntity'] = relationship(post_update=True)

    post_id = mapped_column(ForeignKey("post.id"))
    post: Mapped['PostEntity'] = relationship(back_populates="comments", post_update=True)

    # not sure ifi this line is necessary, i am combining kris jordan's and my own code
    # replyTo_id = mapped_column(ForeignKey("comments.id"))
    replies: Mapped[list["CommentEntity"]] = relationship(secondary="reply", primaryjoin=id==reply_table.c.comment_id,
                            secondaryjoin=id==reply_table.c.reply_id, back_populates="replies", post_update=True)
    
    text: Mapped[str] = mapped_column(String(64))
    created: Mapped[datetime] = mapped_column(DateTime)

    @classmethod
    def from_model(cls, model: Comment) -> Self:
        return cls(
            id=model.id,
            text=model.text,
            created=model.created,
            commenter=model.commenter,
            post=model.post,
            replies=model.replies
        )

    def to_model(self) -> Comment:
        return Comment(
            id=self.id,
            text=self.text,
            commenter=self.commenter,
            created=self.created,
            post=self.post,
            replies=self.replies,
        )

    # not sure if necessary
    # def update(self, model: Post) -> None:
    #     self.content = model.content
    #     self.tags = model.tagss
