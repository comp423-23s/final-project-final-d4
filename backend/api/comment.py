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
@api.delete("/{post_id}/{comment_id}")
def delete_comment(post_id: int, comment_id: int, user = Depends(registered_user), comment_service = Depends(CommentService)) -> None:
    try:
        return comment_service.delete(user,post_id,comment_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    