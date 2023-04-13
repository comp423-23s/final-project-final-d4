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
    content: str=""
    tags: list[str] = []
    created: datetime = datetime.now()
    title: str = ""
    description: str = ""
    pid: int | None = None

class NewPost(BaseModel):
    content: str=""
    tags: list[str] = []
    created: datetime = datetime.now()
    title: str = ""
    description: str = ""

# copied fro professor's databse code at the end of User Model.. Assuming theres some importance here
# Python... :sob:... necessary due to circularity (TODO: refactor to remove circularity)
# from .comment import Comment
Post.update_forward_refs()
NewPost.update_forward_refs()
