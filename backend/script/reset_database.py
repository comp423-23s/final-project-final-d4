"""Reset the database by dropping all tables, creating tables, and inserting demo data."""

import sys
from sqlalchemy import text
from sqlalchemy.orm import Session
from ..database import engine
from ..env import getenv
from .. import entities

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


if getenv("MODE") != "development":
    print("This script can only be run in development mode.", file=sys.stderr)
    print("Add MODE=development to your .env file in workspace's `backend/` directory")
    exit(1)


# Reset Tables
entities.EntityBase.metadata.drop_all(engine)
entities.EntityBase.metadata.create_all(engine)


# Insert Dev Data from `script.dev_data`

# Add Users
with Session(engine) as session:
    from .dev_data import users
    to_entity = entities.UserEntity.from_model
    session.add_all([to_entity(model) for model in users.models])
    session.execute(text(f'ALTER SEQUENCE {entities.UserEntity.__table__}_id_seq RESTART WITH {len(users.models) + 1}'))
    session.commit()

# Add Roles
with Session(engine) as session:
    from .dev_data import roles
    to_entity = entities.RoleEntity.from_model
    session.add_all([to_entity(model) for model in roles.models])
    session.execute(text(f'ALTER SEQUENCE {entities.RoleEntity.__table__}_id_seq RESTART WITH {len(roles.models) + 1}'))
    session.commit()

# Add Users to Roles
with Session(engine) as session:
    from ..entities import UserEntity, RoleEntity
    from .dev_data import user_roles
    for user, role in user_roles.pairs:
        user_entity = session.get(UserEntity, user.id)
        role_entity = session.get(RoleEntity, role.id)
        user_entity.roles.append(role_entity)
    session.commit()

# Add Permissions to Users/Roles
with Session(engine) as session:
    from ..entities import PermissionEntity
    from .dev_data import permissions
    for role, permission in permissions.pairs:
        entity = PermissionEntity.from_model(permission)
        entity.role = session.get(RoleEntity, role.id)
        session.add(entity)
    session.execute(text(f'ALTER SEQUENCE permission_id_seq RESTART WITH {len(permissions.pairs) + 1}'))
    session.commit()

# Add Posts to Post table
with Session(engine) as session:
    from ..entities import PostEntity
    from .dev_data import post
    to_entity = entities.PostEntity.from_model
    session.add_all([to_entity(post) for post in post.post_models])
    session.execute(text(f'ALTER SEQUENCE {entities.PostEntity.__table__}_id_seq RESTART WITH {len(post.post_models) + 1}'))
    session.commit()

# Add Users to Posts
with Session(engine) as session:
    from ..entities import UserEntity, PostEntity
    from .dev_data import user_posts
    for user, post in user_posts.pairs:
        user_entity = session.get(UserEntity, user.id)
        post_entity = session.get(PostEntity, post.id)
        user_entity.userPosts.append(post_entity)
    session.commit()

# Add Comments to Comment table
with Session(engine) as session:
    from ..entities import CommentEntity
    from .dev_data import comments
    to_entity = entities.CommentEntity.from_model
    session.add_all([to_entity(comment) for comment in comments.comment_models])
    session.execute(text(f'ALTER SEQUENCE {entities.CommentEntity.__table__}_id_seq RESTART WITH {len(comments.comment_models) + 1}'))
    session.commit()

# Add Comments to Posts
with Session(engine) as session:
    from ..entities import CommentEntity, PostEntity
    from .dev_data import post_comments, comments
    for comments, post in post_comments.pairs:
        comment_entity = session.get(CommentEntity, comments.id)
        post_entity = session.get(PostEntity, post.id)
        post_entity.comments.append(comment_entity)
    session.commit()