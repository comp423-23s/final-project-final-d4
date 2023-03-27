from sqlalchemy import Table, Column, ForeignKey
from .entity_base import EntityBase

#comment reply
reply_table = Table(
    "reply", 
    EntityBase.metadata,
    Column('comment_id', ForeignKey('comments.id'), primary_key=True),
    Column('reply_id', ForeignKey('comments.id'), primary_key=True)
)