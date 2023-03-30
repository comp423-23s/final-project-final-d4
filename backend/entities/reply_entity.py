from sqlalchemy import Table, Column, ForeignKey
from .entity_base import EntityBase

#comment reply
reply_table = Table(
    "reply", 
    EntityBase.metadata,
    Column('comment_id', ForeignKey('comment.id'), primary_key=True),
    Column('reply_id', ForeignKey('comment.id'), primary_key=True)
)