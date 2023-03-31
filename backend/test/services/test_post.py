import pytest

from sqlalchemy.orm import Session
from ...models import Post, Team, Comment, User
from ...services import PostService

# Model post 
sample_post = Post(id=1, content="Welcome to csxl!", postedBy=1, comments=[])
false_post = Post(id=2, postedBy=2,content="")
# Model comment
sample_comment_1 = Comment(id=1, commenter=1, text="Hello", post=1, replies=[])
# Model user
user = User(id=3, pid=111111111, onyen='user', email='user@unc.edu')
# Model team
team_1 = Team(id=1, members=[user], project="1")


def test_create_post_valid(post: PostService):
    post.create_post(sample_post)
    assert(post.get_posts() != None)


def test_create_post_invalid_content(post: PostService):
    with pytest.raises(Exception):         
        post.create_post(false_post)

