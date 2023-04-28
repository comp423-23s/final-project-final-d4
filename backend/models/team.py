"""Team model serves as the data object for representing teams of students across application layers."""

from pydantic import BaseModel
from datetime import datetime

#: Post object
class Team(BaseModel):
    # this is the primary key
    id: int | None = None
    members: list['User'] = []
    project: str = ""

# copied fro professor's databse code at the end of User Model.. Assuming theres some importance here
# Python... :sob:... necessary due to circularity (TODO: refactor to remove circularity)
from .user import User
Team.update_forward_refs()
