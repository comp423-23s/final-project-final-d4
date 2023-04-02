"""Post model serves as the data object for representing posts across application layers."""

from pydantic import BaseModel
from datetime import datetime

# not sure if i need this lol
# __authors__ = ["Chalisa Phoomsakha"]
# __copyright__ = "Copyright 2023"
# __license__ = "MIT"

#: Post object
class Post(BaseModel):
    # this is the primary key
    id: int | None = None
    content: str = ""
    created: datetime = datetime.now()
    postedBy: int | None # postedBy = userID
    comments: list['Comment'] = []
    tags: list[str] = []
    title: str = ""
    description: str = ""
    # class Config:
    #     orm_mode = True

# copied fro professor's databse code at the end of User Model.. Assuming theres some importance here
# Python... :sob:... necessary due to circularity (TODO: refactor to remove circularity)
from .user import User
from .comment import Comment
Post.update_forward_refs()