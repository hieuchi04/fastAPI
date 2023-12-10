from pydantic import BaseModel
from fastapi.responses import JSONResponse
from configs.mysql_config import My_Connection


class ReportComment(BaseModel):
    id_report: int
    id_comment: int
    report_reason: str
    content: str
    id_user_report: int
    id_user_comment: int


class ReportCommentModel:

    def get_comments(self):
        with My_Connection() as db_connection:
            cur = db_connection.cur
            cur.execute("select * from report_comment")
            result = cur.fetchall()
            return JSONResponse(result)
