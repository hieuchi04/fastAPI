from fastapi import Query, Request, APIRouter
from model.comment_model import CommentModel

router = APIRouter()
obj = CommentModel()


@router.get("/api/comments")
def get_comments(content: str = Query(default=None), ip_comment: str = Query(default=None),
                 user_name: str = Query(default=None)):
    return obj.get_comments(content, ip_comment, user_name)


@router.delete("/api/comments/{cid}")
def delete_comment(cid: int):
    return obj.delete_comment(cid)


@router.patch("/api/comments/{cid}")
async def edit_comment(cid: int, request: Request):
    form_data = await request.form()
    return obj.edit_comment(form_data, cid)
