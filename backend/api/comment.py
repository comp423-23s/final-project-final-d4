from fastapi import APIRouter, HTTPException, Depends
from ..services import CommentService
from ..models import Comment


api = APIRouter()

#api route retrieces ALL comments
@api.get("/api/comments")
def get_comments(comment_service: CommentService = Depends()) -> list[Comment]:
    return comment_service.all()

#api route creates a new comment
@api.post("/api/comment")
def new_comment(comment: Comment, comment_service: CommentService = Depends()) -> Comment:
        try:
            return comment_service.create(comment)
        except Exception as e:
            raise HTTPException(status_code=422, detail=str(e))
        
#api route deletes comment
@api.delete("/api/delete/comment/{id}")
def delete_comment(id: int, comment_service = Depends(CommentService)):
    try:
        return comment_service.delete(id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
#api route to update a comment's text
@api.post("/api/comment/edit")
def update_comment(comment_id: int, newText: str, comment_service: CommentService = Depends()) -> Comment:
    try:
        return comment_service.update(comment_id, newText)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
    
#api route to reply to a comment
@api.post("/api/reply")
def create_reply(comment_id: int, reply: Comment, comment_service: CommentService = Depends()) -> Comment:
    try: 
        return comment_service.reply(comment_id=comment_id,reply=reply)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
