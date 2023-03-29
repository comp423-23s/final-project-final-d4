'''Team accounts for all registered users in the application.'''


from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self
from .entity_base import EntityBase
from .membership_entity import membership_table
from ..models import Team


# __authors__ = ['Chalisa Phoomsakha']
# __copyright__ = 'Copyright 2023'
# __license__ = 'MIT'


class TeamEntity(EntityBase):
    __tablename__ = 'team'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project: Mapped[str] = mapped_column(String(64), unique=True, index=True, default='')

    
    members: Mapped[list['UserEntity']] = relationship(secondary=membership_table, back_populates='teams')

    @classmethod
    def from_model(cls, model: Team) -> Self:
        return cls(
            project=model.project,
            members=model.members,
        )

    def to_model(self) -> Team:
        return Team(
            project=self.project,
            members=self.members,
        )

    def update(self, model: Team) -> None:
        self.project = model.project
        self.members = model.members
