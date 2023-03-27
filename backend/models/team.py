"""Team model serves as the data object for representing teams of students across application layers."""

from pydantic import BaseModel
from datetime import datetime

# not sure if i need this lol
# __authors__ = ["Chalisa Phoomsakha"]
# __copyright__ = "Copyright 2023"
# __license__ = "MIT"

#: Post object
class Team(BaseModel):
    # this is the primary key
    id: int | None = None
    # not sure if we need to track this
    # created: datetime
    members = list['User'] = []
    project = str = ""
    # class Config:
    #     orm_mode = True

# copied fro professor's databse code at the end of User Model.. Assuming theres some importance here
# Python... :sob:... necessary due to circularity (TODO: refactor to remove circularity)
from .user import User
Team.update_forward_refs()
