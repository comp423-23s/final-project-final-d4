from fastapi import APIRouter, HTTPException, Depends

from backend.models.comment import NewComment
from ..services import CommentService
from ..models import Comment
from .authentication import registered_user


api = APIRouter(prefix="/api/comment")

#api route retrieces ALL comments
@api.get("/{post_id}", response_model=list[Comment])
def get_comments(user = Depends(registered_user), comment_service: CommentService = Depends(),post_id=int) -> list[Comment]:
    return comment_service.all(user,post_id)

#api route creates a new comment
@api.post("/{post_id}")
def new_comment(comment: NewComment, post_id: int, user = Depends(registered_user), comment_service: CommentService = Depends()) -> Comment:
        try:
            return comment_service.create(user,comment,post_id)
        except Exception as e:
            raise HTTPException(status_code=422, detail=str(e))
        
#api route deletes comment
@api.delete("/{id}")
def delete_comment(id: int, user = Depends(registered_user), comment_service = Depends(CommentService)):
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
@api.post("/reply")
def create_reply(comment_id: int, reply: Comment, comment_service: CommentService = Depends()) -> Comment:
    try: 
        return comment_service.reply(comment_id=comment_id,reply=reply)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
