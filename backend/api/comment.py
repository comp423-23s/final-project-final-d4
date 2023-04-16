"""This module provides a RESTful API for interacting with the comment application.

Endpoints:
- GET /comment/{post_id} - Retrieve comments for a specific post.
- POST /comment - Create a new comment.
- DELETE /comment/{id} - Delete a comment.

Usage:
import comment
"""
from fastapi import APIRouter, HTTPException, Depends
from ..services import CommentService
from ..models import Comment
from .authentication import registered_user


api = APIRouter(prefix="/api/comment")

#api route retrieces ALL comments
@api.get("/{post_id}", response_model=list[Comment])
def get_comments(user = Depends(registered_user), comment_service: CommentService = Depends(),post_id=int) -> list[Comment]:
    """API endpoint for retrieving all comments on a post.

    Parameters:
    - user (Depends): dependency injection for retrieving the currently logged-in user
    - comment_service (CommentService): dependency injection for the CommentService class
    - post_id (int): the ID of the post to retrieve comments for

    Returns:
    - list[Comment]: a list of Comment objects representing all comments on the specified post

    HTTP Methods:
    - GET

    Usage:
    - Send a GET request to the endpoint with the post ID as a URL parameter
    - Returns a list of Comment objects representing all comments on the specified post
    """
    return comment_service.all(user,post_id)

#api route creates a new comment
@api.post("")
def new_comment(comment: Comment, user = Depends(registered_user), comment_service: CommentService = Depends()) -> Comment:
    """API endpoint for creating a new comment.

    Parameters:
    - comment (Comment): the Comment object representing the new comment to create
    - user (Depends): dependency injection for retrieving the currently logged-in user
    - comment_service (CommentService): dependency injection for the CommentService class

    Returns:
    - Comment: the newly created Comment object

    HTTP Methods:
    - POST

    Usage:
    - Send a POST request to the endpoint with a Comment object representing the new comment in the request body
    - Returns the newly created Comment object if successful
    - Raises an HTTPException with status code 422 and a detailed error message if the creation fails
    """
    try:
        return comment_service.create(user,comment)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
        
#api route deletes comment
@api.delete("/{id}")
def delete_comment(id: int, user = Depends(registered_user), comment_service = Depends(CommentService)):
    """API endpoint for deleting a comment.

    Parameters:
    - id (int): the ID of the comment to delete
    - user (Depends): dependency injection for retrieving the currently logged-in user
    - comment_service (CommentService): dependency injection for the CommentService class

    Returns:
    - None

    HTTP Methods:
    - DELETE

    Usage:
    - Send a DELETE request to the endpoint with the comment ID as a URL parameter
    - Deletes the specified comment if successful
    - Raises an HTTPException with status code 404 and a detailed error message if the comment is not found
    """
    try:
        return comment_service.delete(user,id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
#api route to update a comment's text
# @api.post("/api/comment/edit")
# def update_comment(comment_id: int, newText: str, comment_service: CommentService = Depends()) -> Comment:
#     try:
#         return comment_service.update(comment_id, newText)
#     except Exception as e:
#         raise HTTPException(status_code=422, detail=str(e))
    
#api route to reply to a comment
# @api.post("/reply")
# def create_reply(comment_id: int, reply: Comment, comment_service: CommentService = Depends()) -> Comment:
#     try: 
#         return comment_service.reply(comment_id=comment_id,reply=reply)
#     except Exception as e:
#         raise HTTPException(status_code=422, detail=str(e))
