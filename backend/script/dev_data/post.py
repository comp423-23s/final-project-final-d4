"""Sample posts for post list."""

from ...models import Post


post_1 = Post(id=1, content="Good", tags=["Project"], title="Find Teammates!", description="Test")
post_2 = Post(id=2, content="Good", tags=["Share insights"], title="Google just published its ChatGPT", description="Test")
post_3 = Post(id=3, content="Good", tags=["Backend"], title="How to master backend", description="Test")
post_4 = Post(id=4, content="Good", tags=["Frontend"], title="Check out this fun frontend design", description="Test")


post_models = [
    post_1, 
    post_2, 
    post_3,
    post_4
]