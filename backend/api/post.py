"""This module provides a RESTful API for interacting with the post application.

Endpoints:
- GET /post - Retrieve all post for generating post list.
- GET /post/{search_string} - Search for posts that has content, description, title that match with the search string.
- POST /post - Create a post.
- DELETE /post/{id} - Delete a post.

Usage:
import post
"""

from fastapi import APIRouter, Depends, HTTPException
from ..services.post import PostService
from ..models.post import Post, NewPost
from ..models import User
from .authentication import registered_user

openapi_tags = {"name": "Post view", "description": "Post projects endpoints."}

api = APIRouter(prefix="/api/post")

@api.get("", tags=["Post"])
def get_posts(post_serv: PostService = Depends()) -> list[Post]:
    """API endpoint for retrieving all posts to generate post list view.

    Parameters:
    - post_serv: dependency injection from the post service 

    Returns:
    - list[Post]: a list of Post objects representing all post in the post table

    HTTP Methods:
    - GET

    Usage:
    - Send a GET request to the endpoint api/post
    - Returns a list of Post objects representing all post in the post table
    """
    return post_serv.get_posts()

@api.get("/{search_string}", response_model=list[Post], tags=["Post"])
def search_post(search_string: str, post_serv: PostService = Depends()) -> list[Post]:
    """API endpoint for retrieving posts that has content, description, title that match with the search string.

    Parameters:
    - search_string: a string literal used as a search criteria
    - post_serv: dependency injection from the post service 

    Returns:
    - list[Post]: a list of Post objects that has content, title, description that match the search string

    HTTP Methods:
    - GET

    Usage:
    - Send a GET request to the endpoint api/post/{search_string}
    - Return a list of Post objects that has content, title, description that match the search string
    """
    try:
        return post_serv.search_post(search_string)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@api.post("", tags=["Post"])
def create_post(post: NewPost, post_serv: PostService = Depends(), subject: User = Depends(registered_user)) -> Post:
    """
    API endpoint for creating a new post.

    Parameters:
    - post: the NewPost object representing the new post to create
    - post_serv: dependency injection from the post service
    - subject: dependency injection for retrieving the currently logged-in user

    Returns:
    - Post: the newly created Post object

    HTTP Methods:
    - POST

    Usage:
    - Send a POST request to the endpoint api/post with a NewPost object representing the new post in the request body
    - Returns the newly created Post object if successful
    """
    try:
        return post_serv.create_post(post, subject)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@api.delete("/{id}",tags=["Post"])
def delete_post(id:int, post_serv: PostService = Depends(), subject: User = Depends(registered_user)) -> Post:
    """
    API endpoint for deleting a post.
    
    Parameters:
    - id: the id of the post to delete
    - post_serv: dependency injection from the post service
    - subject: dependency injection for retrieving the currently logged-in user

    Returns:
    - Post: the deleted Post object

    HTTP Methods:
    - DELETE

    Usage:
    - Send a DELETE request to the endpoint api/post/{id}
    - Returns the deleted Post object if successful
    """
    try:
        return post_serv.delete_post(subject, id)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
    
#api route to update user info
@api.put("/{id}", tags=["Post"])
def update_post(id: int, 
                content: str | None,
                title: str | None, 
                description: str | None, 
                tags: list[str] | None,
                post_serv: PostService = Depends(),
                subject: User = Depends(registered_user)) -> Post:
    """
    API endpoint for updating a post.
    
    Parameters:
    - id: the id of the post to update
    - content: optional new content for post
    - title: optional new title for post
    - description: optional description for post
    - tags: optional new tags for post
    - post_serv: dependency injection from the post service

    Returns:
    - Post: the updated Post object

    HTTP Methods:
    - PUT

    Usage:
    - Send a PUT request to the endpoint api/post/{id}
    - Returns the updated Post object if successful
    """
    try:
        return post_serv.update(subject=subject, id=id, content=content, title=title, description=description, tags=tags)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))