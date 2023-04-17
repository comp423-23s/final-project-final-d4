"""Sample posts for post list."""

from ...models import Comment


comment_1 = Comment(id=1, commenter=100000000, text="test comment",post=1, private=False)
comment_2 = Comment(id=2, commenter=100000000, text="test comment2",post=1, private=False)
comment_3 = Comment(id=1, commenter=100000001, text="test comment3",post=2, private=False)
comment_4 = Comment(id=2, commenter=100000001, text="test comment4",post=3, private=False)


comment_models = [
    comment_1, 
    comment_2, 
    comment_3,
    comment_4
]

