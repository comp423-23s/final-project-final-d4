
"""Sample comments for comment list."""

from ...models import Comment

comment_1 = Comment(id=1, commenter=100000000, post=1, text="test comment1 what an interesting topic!", private=False)
comment_2 = Comment(id=2, commenter=100000000, post=1, text="test comment2 I'd love to know more!", private=False)
comment_3 = Comment(id=3, commenter=100000001, post=2, text="test comment3 I like your viewpoints!",private=False)
comment_4 = Comment(id=4, commenter=100000001, post=3, text="test comment4 This is very useful, thx!",private=False)

comment_models = [
    comment_1, 
    comment_2, 
    comment_3,
    comment_4
]

