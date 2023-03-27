"""Comment model serves as the data object for representing comments across application layers."""

from pydantic import BaseModel
from datetime import datetime

# not sure if i need this lol
# __authors__ = ["Chalisa Phoomsakha"]
# __copyright__ = "Copyright 2023"
# __license__ = "MIT"

#: Comments
class Comment(BaseModel):
    id: int | None = None
    commenter: 'User' | str
    post: 'Post' | int
    replies: list['Comment'] = []
    text: str = ""
    created: datetime
    # class Config:
    #     orm_mode = True

# copied from professor's databse code at the end of User Model.. Assuming theres some importance here
# Python... :sob:... necessary due to circularity (TODO: refactor to remove circularity)
from .user import User
from .post import Post
Comment.update_forward_refs()