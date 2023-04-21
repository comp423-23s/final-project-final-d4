from fastapi import Depends
import pytest

from backend.services.permission import UserPermissionError
from .permission_test import permission

from sqlalchemy.orm import Session

from ...services import PermissionService
from ...models import Post, Comment, User, Role, Permission
from ...models.post import NewPost
from ...models.comment import NewComment
from ...services import PostService, UserService, CommentService
from ...entities import UserEntity, PostEntity, RoleEntity, PermissionEntity,CommentEntity


# Model post 
sample_post = NewPost(content="Good Day", tags=["Daily"], title="Greeting", description="Good morrow students!")
sample_post_2 = NewPost(content="Good Day", tags=["Daily"], title="Greeting", description="Good morrow students!")

# Model user
root = User(id=1, pid=999999999, onyen='root', email='root@unc.edu')
root_role = Role(id=1, name='root')

ambassador = User(id=2, pid=888888888, onyen='ambassador',
                  email='ambassador@unc.edu')
ambassador_role = Role(id=2, name='ambassadors')
ambassador_permission: Permission

user = User(id=3, pid=111111111, onyen='user', email='user@unc.edu')
unregistered = User(id=4, pid=111111112, onyen='user2', email='user2@unc.edu')

# Model comment
sample_comment_1 = NewComment(post=1,text="Hello",private=True)
sample_comment_2 = NewComment(post=1,text="Hello2",private=False)

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
    root_permission_entity_post = PermissionEntity(
        action='post.delete', resource='*', role=root_role_entity)
    test_session.add(root_permission_entity)
    test_session.add(root_permission_entity_post)

    # Bootstrap user and ambassador without any special perms
    user_entity = UserEntity.from_model(user)
    test_session.add(user_entity)
    ambassador_entity = UserEntity.from_model(ambassador)
    test_session.add(ambassador_entity)

    test_session.commit()


@pytest.fixture
def post(test_session: Session):
    return PostService(session=test_session,permission=permission)

@pytest.fixture()
def users(test_session: Session):
    return UserService(session=test_session, permission=permission)

@pytest.fixture()
def permission(test_session: Session):
    return PermissionService(test_session)

@pytest.fixture()
def comment(test_session: Session):
    return CommentService(test_session)

# get post test
def test_get_post(post: PostService):
    assert(len(post.get_posts()) == 0)

# creat post test
def test_create_post(post: PostService, test_session: Session, users: UserService):
    post.create_post(sample_post, user)
    assert(len(post.get_posts()) == 1)

def test_create_post_invalid_user(post: PostService):
    with pytest.raises(ValueError):
        post.create_post(sample_post, unregistered)

# delete post test
def test_delete_post_valid(post: PostService,users: UserService, test_session: Session):
    post.create_post(sample_post, user)
    post.delete_post(user, 1)
    assert(len(post.get_posts())==0)

def test_delete_post_valid_admin(post: PostService,users: UserService, test_session: Session):
    post.create_post(sample_post, user)
    post.delete_post(root, 1)
    assert(len(post.get_posts())==0)

def test_delete_post_invalid_userpermission(post: PostService):
    post.create_post(sample_post, user)
    with pytest.raises(UserPermissionError):
        post.delete_post(ambassador, 1)

# search post test
def test_search_post(post: PostService):
    post.create_post(sample_post, user)
    sample = post.search_post("greeting")
    assert(len(sample) == 1)
    
    post.create_post(sample_post_2, user)
    sample_2 = post.search_post("Greeting")
    assert(len(sample_2) == 2)

def test_update_post(post: PostService):
    post.create_post(sample_post, user)
    newPost = post.update(user, 1, "test", "test", "test", ["test"])
    savedPost = post.get_posts()[0]
    assert(savedPost.content == newPost.content)
# Test for comment part

# get comment test
def test_get_comment(post: PostService, comment: CommentService):
    post.create_post(sample_post, user)
    assert(len(comment.all(user,1)) == 0)

# create comment test
def test_create_comment_private(post: PostService, comment: CommentService):
    post.create_post(sample_post,user)
    comment.create(user,sample_comment_1,1)
    assert(len(comment.all(user,1)) == 1)
    assert(len(comment.all(ambassador,1)) == 0)

def test_create_comment_notprivate(post: PostService, comment: CommentService):
    post.create_post(sample_post,user)
    comment.create(user,sample_comment_2,1)
    assert(len(comment.all(user,1)) == 1)
    assert(len(comment.all(ambassador,1)) == 1)

def test_create_comment_invalid_postid(post: PostService, comment: CommentService):
    post.create_post(sample_post,user)
    sample_comment = NewComment(text="Hello",private=False)
    with pytest.raises(ValueError):
        comment.create(user,sample_comment,6)

# delete comment test
def test_delete_comment_valid_author_private(post: PostService, comment: CommentService):
    post.create_post(sample_post,user)
    comment.create(user,sample_comment_1,1)
    assert(len(comment.all(user,1)) == 1)
    comment.delete(user,1,1)
    assert(len(comment.all(user,1)) == 0)

def test_delete_comment_valid_author_notprivate(post: PostService, comment: CommentService):
    post.create_post(sample_post,user)
    comment.create(user,sample_comment_2,1)
    assert(len(comment.all(user,1)) == 1)
    comment.delete(user,1,1)
    assert(len(comment.all(user,1)) == 0)

def test_delete_comment_invalid_id(post: PostService, comment: CommentService):
    post.create_post(sample_post,user)
    comment.create(user,sample_comment_1,1)
    with pytest.raises(ValueError):
        comment.delete(user,5,5)

def test_delete_comment_valid_admin(post: PostService, comment: CommentService):
    post.create_post(sample_post,user)
    comment.create(user,sample_comment_1,1)
    comment.delete(root,1,1)
    assert(len(comment.all(user,1)) == 0)

def test_delete_comment_invalid_notauthor(post: PostService, comment: CommentService):
    post.create_post(sample_post,user)
    comment.create(user,sample_comment_2,1)
    with pytest.raises(UserPermissionError):
        comment.delete(ambassador,1,1)

def test_delete_comment_invalid_private_notauthor(post: PostService, comment: CommentService):
    post.create_post(sample_post,user)
    comment.create(user,sample_comment_1,1)
    comment.delete(ambassador,1,1)
    assert(len(comment.all(user,1)) == 1)