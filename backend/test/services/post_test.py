from fastapi import Depends
import pytest

from sqlalchemy.orm import Session

from backend.services.permission import PermissionService
from ...models import Post, Comment, User
from ...services import PostService,UserService

# Model post 
sample_post = Post(id=1, content="Welcome to csxl!", postedBy=111111111, comments=[], title="test",description="test")
# Model comment
sample_comment_1 = Comment(id=1, commenter=1, text="Hello", post=1, replies=[])
# Model user
user1 = User(id=1, pid=111111111, onyen='user', email='user@unc.edu')

def create_session():
    with Session() as session:
        yield session

SessionDependency = Depends(create_session)

@pytest.fixture
def post():
    # Create a PostService object and return it as the fixture value
    permission_service = PermissionService()
    return PostService(session=SessionDependency,permission=permission_service)

def test_empty_post(post: PostService):
    assert(len(post.get_posts()) == 4)


# def test_add_post_invalid_pid(post: PostService):
#     with pytest.raises(Exception):
#         post.create_post(sample_post)
    
#     assert(len(post.get_posts()) == 0)
