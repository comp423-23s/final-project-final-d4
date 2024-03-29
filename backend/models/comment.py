"""Comment model serves as the data object for representing comments across application layers."""

from pydantic import BaseModel
from datetime import datetime

#: Comments
class Comment(BaseModel):
    id: int | None = None
    # commenter is the pid of the user
    commenter: int | None
    post: int
    # replies: list['Comment'] = []
    text: str = ""
    created: datetime = datetime.now()
    private: bool

class NewComment(BaseModel):
    id: int | None = None
    text: str = ""
    created: datetime = datetime.now()
    private: bool

# copied from professor's databse code at the end of User Model.. Assuming theres some importance here
# Python... :sob:... necessary due to circularity (TODO: refactor to remove circularity)
from .user import User
from .post import Post
Comment.update_forward_refs()
NewComment.update_forward_refs()