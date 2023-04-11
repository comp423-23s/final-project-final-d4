from fastapi import Depends
import pytest

from sqlalchemy.orm import Session

from backend.services.permission import PermissionService
from ...models import Post, Comment, User
from ...services import PostService,UserService
from ...entities import UserEntity, PostEntity

# Model post 
sample_post = Post(id=5,content="Good Day", tags=["Daily"], title="Greeting", description="Good morrow students!")

# Model user
user1 = User(id=5, pid=999999998, onyen="one", first_name="abc", last_name="abc", email="abc@unc.edu", pronouns="she/her/hers")

# Model comment
sample_comment_1 = Comment(id=1, commenter=1, text="Hello", post=1, replies=[])


# def create_session():
#     with Session() as session:
#         yield session

# SessionDependency = Depends(create_session)

@pytest.fixture
def post(test_session: Session):
    # Create a PostService object and return it as the fixture value
    permission_service = PermissionService(test_session)
    return PostService(session=test_session,permission=permission_service)

def test_empty_post(post: PostService):
    assert(len(post.get_posts()) == 4)

def test_create_post(post: PostService, test_session: Session):
    user_1_entity = UserEntity.from_model(user1)
    test_session.add(user_1_entity)
    post.create_post(sample_post, user1)
    assert(len(post.get_posts()) == 5)

def test_delete_post_valid(post: PostService):
    post.delete_post(4)
    assert(len(post.get_posts())==4)
