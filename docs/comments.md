# Comments

## Overview
The comment feature provides functionality for creating, retrieving, and deleting comments on posts. It primarily serves for users who are interested in the post and wants to discuss with other users. This feature allows the community to be more interactive and friendly.

This feature contains the following three operations.

**View Comment**: Everyone can see public comments. If a comment is private, only the author of the post, the author of the comment, and the admin can see it.

**Create Comment**: A CSXL user can create a comment under a post. The create comment can be found if the user click into the post he or she wants to comment.

**Delete Comment**: Only the author of the comment and the admin are allowed to delete the comment under a post.

## Implementation Notes
Each comment has features of commenter, post_id, text, created time, and private indicator. The commenter represents the author of the comment; the post_id represents which post the comment is under; text is the content of teh comment; created time is the time the comment is posted. 

And the interesting design choice is the private indicator. We thought about the possibility that when a post is about finding teammates for project, it is not cyberly safe for users to type their information in the comment publicly. We choose to add a private feature to comments over adding a communication system to the website becuase we know most people still prefer to communicate using texts, slack, and other ways. By allowing users to create private comments, they can exchange their information safely.

## Development Concerns
If a new developer wanted to start working on comment feature, be aware of the following points:

**Backend**
1. There is a permission check needed for retrieving comments. If the comment is private, then only the author of the post, the author of the comment, and the admin can access it. You can take a close look at the comment.py in backend/services.
2. There are two comment models. One is Comment and the other is NewComment. The difference is that the NewComment model matches with the frontend. The info we received from frontend is NewComment, and the model we are recording in the database is Comment. The model Comment contains information like commenter and post_id that the NewComment does not have. You can take a close look at comment.py in backend/models and comment_entity.py in backend/entities.

**Frontend**
1. The frontend implementation is in frontend/src/app/post-details and the corresponding service file is in comments.service in frontend directory
2. The create comment function sends the newComment model to the backend. All functions in the backend would sent Comment related model back to the frontend.


You can also add reply to comments when you get started to make it more interactive.

## Future Work
Currently, there is a 422 bug when creating a comment. It seems that the problem is the isPrivate argument is not transported to the backend properly. We need to work on this in the following days.

The comment feature can be more interesting if we can add reactions such as like or dislike just like a forum. Given more time, we would add this feature in it.

