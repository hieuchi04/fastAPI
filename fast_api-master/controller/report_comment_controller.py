from fastapi import Query, Request, APIRouter
from model.report_comment_model import ReportCommentModel

router = APIRouter()
obj = ReportCommentModel()


@router.get('/api/report-comments')
def get_report_comments():
    return obj.get_comments()
