from pydantic import BaseModel
from fastapi.responses import JSONResponse
from configs.mysql_config import My_Connection


class Comment(BaseModel):
    noi_dung_comment: str
    IP_Comment: str
    device_Comment: str
    id_toan_bo_su_kien: str
    imageattach: str
    thoi_gian_release: str
    id_user: int
    user_name: str
    avatar_user: str
    so_thu_tu_su_kien: int
    location: str


class CommentModel:

    def get_comments(self, content: str, ip_comment: str, user_name: str):
        conditions = []
        params = {}

        if content:
            conditions.append("noi_dung_Comment LIKE %(content)s")
            params['content'] = f"%{content}%"
        if ip_comment:
            conditions.append("IP_Comment LIKE %(ip_comment)s")
            params['ip_comment'] = f"%{ip_comment}%"
        if user_name:
            conditions.append("user_name LIKE %(user_name)s")
            params['user_name'] = f"%{user_name}%"

        sql = "SELECT * FROM comment"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        with My_Connection() as db_connection:
            db_connection.cur.execute(sql, params)
            result = db_connection.cur.fetchall()
            if result:
                return result
            return {"message": "No data found"}

    def delete_comment(self, cid: int):
        with My_Connection() as db_connection:
            db_connection.cur.execute("DELETE FROM comment WHERE id_Comment = %(cid)s", {"cid": cid})
            if db_connection.cur.rowcount > 0:
                return {"message": "DELETED_SUCCESSFULLY"}
            return {"message": "CONTACT_DEVELOPER"}

    def edit_comment(self, data, cid: int):
        sql = (
            "UPDATE comment SET noi_dung_Comment=%s WHERE id_Comment=%s"
        )

        values = (
            data.get('noi_dung_Comment', None),
            cid
        )
        with My_Connection() as db_connection:
            db_connection.cur.execute(sql, values)
            if db_connection.cur.rowcount > 0:
                return JSONResponse({"message": "UPDATED_SUCCESSFULLY"}, 201)
            else:
                return JSONResponse({"message": "NOTHING_TO_UPDATE"}, 204)
