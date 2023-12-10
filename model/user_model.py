from pydantic import BaseModel
from fastapi.responses import JSONResponse
from configs.mysql_config import My_Connection


class User(BaseModel):
    link_avatar: str
    user_name: str
    ip_register: str
    device_register: str
    password: str
    email: str


class UserModel:

    def get_users(self, email: str, ip_register: str):
        conditions = []
        params = {}

        if email:
            conditions.append("email LIKE %(email)s")
            params['email'] = f"%{email}%"
        if ip_register:
            conditions.append("ip_register LIKE %(ip_register)s")
            params['ip_register'] = f"%{ip_register}%"

        sql = "SELECT * FROM user"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        with My_Connection() as db_connection:
            db_connection.cur.execute(sql, params)
            result = db_connection.cur.fetchall()
            if result:
                return result
            return {"message": "No data found"}

    def get_users_by_comment(self, noi_dung_Comment: str):
        conditions = []
        params = {}

        if noi_dung_Comment:
            conditions.append("comment.noi_dung_Comment LIKE %(noi_dung_Comment)s")
            params['noi_dung_Comment'] = f"%{noi_dung_Comment}%"

        sql = "SELECT user.id_user, user.link_avatar, user.user_name, user.ip_register,user.device_register, user.password, user.email, user.count_comment,user.count_sukien, user.count_view, comment.noi_dung_Comment" \
               " FROM futurelove.user INNER JOIN futurelove.comment ON user.id_user=comment.id_user"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        with My_Connection() as db_connection:
            db_connection.cur.execute(sql, params)
            result = db_connection.cur.fetchall()
            if result:
                return result
            return {"message": "No data found"}


    def add_user_model(self, data: User):
        sql = "INSERT INTO user (link_avatar, user_name, ip_register, device_register, password, email, count_sukien, count_comment, count_view) " \
              "VALUES (%(link_avatar)s, %(user_name)s, %(ip_register)s, %(device_register)s, %(password)s, %(email)s, 0, 0, 0)"

        with My_Connection() as db_connection:
            try:
                db_connection.cur.execute(sql, data.dict())
                if db_connection.cur.rowcount > 0:
                    return JSONResponse(content={"message": "CREATED_SUCCESSFULLY"}, status_code=201)
                else:
                    return JSONResponse(content={"message": "Failed to create user"}, status_code=500)
            except Exception as e:
                # Handle database errors and return an appropriate response
                return JSONResponse(content={"message": "Database error"}, status_code=500)

    def patch_user_model(self, data, uid):
        qry = "UPDATE user SET "
        for key in data:
            if key != 'id_user':
                qry += f"{key}='{data[key]}',"
        qry = qry[:-1] + f" WHERE id_user = {uid}"
        with My_Connection() as db_connection:
            db_connection.cur.execute(qry)
            if db_connection.cur.rowcount > 0:
                return JSONResponse({"message": "UPDATED_SUCCESSFULLY"}, 201)
            else:
                return JSONResponse({"message": "NOTHING_TO_UPDATE"}, 204)

    def delete_user_model(self, uid: int):
        with My_Connection() as db_connection:
            db_connection.cur.execute("DELETE FROM user WHERE id_user = %(uid)s", {"uid": uid})
            if db_connection.cur.rowcount > 0:
                return {"message": "DELETED_SUCCESSFULLY"}
            return {"message": "CONTACT_DEVELOPER"}

    def update_user_model(self, data, uid: int):
        sql = (
            "UPDATE user SET link_avatar=%s, user_name=%s, ip_register=%s, "
            "device_register=%s, password=%s, email=%s WHERE id_user=%s"
        )

        values = (
            data.get('link_avatar', None),
            data.get('user_name', None),
            data.get('ip_register', None),
            data.get('device_register', None),
            data.get('password', None),
            data.get('email', None),
            uid
        )
        with My_Connection() as db_connection:
            db_connection.cur.execute(sql, values)

            if db_connection.cur.rowcount > 0:
                return JSONResponse({"message": "UPDATED_SUCCESSFULLY"}, 201)
            else:
                return JSONResponse({"message": "NOTHING_TO_UPDATE"}, 204)
