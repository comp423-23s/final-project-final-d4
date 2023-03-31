import pytest

from sqlalchemy.orm import Session
from ...models import Post, Team, Comment, User
from ...services import PostService

# Model post 
sample_post = Post(id=1, content="Welcome to csxl!", postedBy=1, comments=[])
# Model comment
sample_comment_1 = Comment(id=1, commenter=1, text="Hello", post=1, replies=[])
# Model user
user = User(id=3, pid=111111111, onyen='user', email='user@unc.edu')
# Model team
team_1 = Team(id=1, members=[user], project="1")

@pytest.fixture(autouse=True)
def test_create_post_valid(post: PostService):
    assert(len(post.get_posts()) == 0)
    
    post.create_post(sample_post)
    assert(len(post.get_posts()) == 1)

    post.create_post(sample_post)
    assert(len(post.get_posts()) == 2)