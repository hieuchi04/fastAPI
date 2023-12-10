from configs.mysql_config import My_Connection
from fastapi.responses import JSONResponse
from jwt_auth.auth_handler import signJWT


class Auth_Model:

    @classmethod
    def change_user_password(cls, data, uid):
        with My_Connection() as db_connection:
            db_connection.cur.execute("SELECT * FROM user WHERE id_user = %(uid)s AND password = %(current_password)s",
                                      {"uid": uid, "current_password": data.get('current_password')})
            result = db_connection.cur.fetchone()

            if result:
                db_connection.cur.execute("UPDATE user SET password = %(new_password)s WHERE id_user = %(uid)s",
                                          {"new_password": data.get('new_password'), "uid": uid})
                return JSONResponse({"message": "Your password successfully updated"}, 200)
            else:
                return JSONResponse({"message": "Current password is incorrect"}, 400)

    @classmethod
    def login_user(self, data):
        with My_Connection() as db_connection:
            query = "SELECT * FROM user WHERE (user_name = %s OR email = %s) AND password = %s"
            db_connection.cur.execute(query, (data['username_or_email'], data['username_or_email'], data['password']))
            result = db_connection.cur.fetchall()

            if len(result) == 1:
                return JSONResponse({"message": "Login successfully", "user": result[0]}, status_code=200)
            else:
                return JSONResponse({"message": "Login failed"}, status_code=401)

    # login_jwt
    # @classmethod
    # def login_user(self, data):
    #     with My_Connection() as db_connection:
    #         query = "SELECT * FROM user WHERE (user_name = %s OR email = %s) AND password = %s"
    #         db_connection.cur.execute(query, (data['username_or_email'], data['username_or_email'], data['password']))
    #         result = db_connection.cur.fetchall()
    #
    #         if len(result) == 1:
    #             jwt_token = signJWT(result[0])
    #             return JSONResponse({"token": jwt_token}, 200)
    #         else:
    #             return JSONResponse({"message": "NO SUCH USER"}, 204)
