"""Sample user/posts pairings."""

from . import users, post

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

pairs = [
    (users.root, post.post_1),
    (users.merritt_manager, post.post_2),
    (users.arden_ambassador, post.post_3),
    (users.root, post.post_4)
]