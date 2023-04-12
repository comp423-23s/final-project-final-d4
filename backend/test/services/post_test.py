from fastapi import Depends
import pytest
from .permission_test import permission

from sqlalchemy.orm import Session

from backend.services.permission import PermissionService
from ...models import Post, Comment, User, Role, Permission
from ...services import PostService,UserService
from ...entities import UserEntity, PostEntity, RoleEntity, PermissionEntity

# Model post 
sample_post = Post(id=1,content="Good Day", tags=["Daily"], title="Greeting", description="Good morrow students!")

# Model user
root = User(id=1, pid=999999999, onyen='root', email='root@unc.edu')
root_role = Role(id=1, name='root')

ambassador = User(id=2, pid=888888888, onyen='ambassador',
                  email='ambassador@unc.edu')
ambassador_role = Role(id=2, name='ambassadors')
ambassador_permission: Permission

user = User(id=3, pid=111111111, onyen='user', email='user@unc.edu')

# Model comment
sample_comment_1 = Comment(id=1, commenter=1, text="Hello", post=1, replies=[])

# def create_session():
#     with Session() as session:
#         yield session

# SessionDependency = Depends(create_session)

@pytest.fixture(autouse=True)
def setup_teardown(test_session: Session):
    # Bootstrap root User and Role
    root_user_entity = UserEntity.from_model(root)
    test_session.add(root_user_entity)
    root_role_entity = RoleEntity.from_model(root_role)
    root_role_entity.users.append(root_user_entity)
    test_session.add(root_role_entity)
    root_permission_entity = PermissionEntity(
        action='*', resource='*', role=root_role_entity)
    test_session.add(root_permission_entity)

    # Bootstrap ambassador and role
    ambassador_entity = UserEntity.from_model(ambassador)
    test_session.add(ambassador_entity)
    ambassador_role_entity = RoleEntity.from_model(ambassador_role)
    ambassador_role_entity.users.append(ambassador_entity)
    test_session.add(ambassador_role_entity)
    ambassador_permission_entity = PermissionEntity(
        action='checkin.create', resource='checkin', role=ambassador_role_entity)
    test_session.add(ambassador_permission_entity)

    # Bootstrap user without any special perms
    user_entity = UserEntity.from_model(user)
    test_session.add(user_entity)

    test_session.commit()

@pytest.fixture
def post(test_session: Session):
    return PostService(session=test_session,permission=permission)

@pytest.fixture()
def users(test_session: Session):
    return UserService(session=test_session, permission=permission)

def test_empty_post(post: PostService):
    assert(len(post.get_posts()) == 0)

def test_create_post(post: PostService, test_session: Session, users: UserService):
    post.create_post(sample_post, user)
    assert(len(post.get_posts()) == 1)

def test_delete_post_valid(post: PostService,users: UserService):
    post.delete_post(1,user)
    assert(len(post.get_posts())==0)