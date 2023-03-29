from sqlalchemy import Table, Column, ForeignKey
from .entity_base import EntityBase

membership_table = Table(
    "membership",
    EntityBase.metadata,
    Column('user_id', ForeignKey('user.id'), primary_key=True),
    Column('team_id', ForeignKey('team.id'), primary_key=True)
)