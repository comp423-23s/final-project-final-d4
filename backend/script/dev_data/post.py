"""Sample posts for post list."""

from ...models import Post

post_1 = Post(id=1, title="Test 1", description="test for story 1", content="test", postedBy=100000000)

post_2 = Post(id=2, title="Test 2", description="test for story 2", content="test", postedBy=100000000)
post_3 = Post(id=3, title="Test 3", description="test for story 3", content="test", postedBy=100000000)
post_4 = Post(id=4, title="Test 4", description="test for story 4", content="test", postedBy=100000000)

post_models = [
    post_1, 
    post_2, 
    post_3,
    post_4
]