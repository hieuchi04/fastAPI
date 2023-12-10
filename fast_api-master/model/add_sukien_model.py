from fastapi import HTTPException
from configs.mysql_config import My_Connection
from fastapi.responses import JSONResponse


class Add_Sukien_Model:
    def get_add_sukiens(self, noidung_sukien: str, ten_sukien: str):
        conditions = []
        params = {}

        if noidung_sukien:
            conditions.append("noidung_sukien LIKE %(noidung)s")
            params['noidung'] = f"%{noidung_sukien}%"
        if ten_sukien:
            conditions.append("ten_sukien LIKE %(ten)s")
            params['ten'] = f"%{ten_sukien}%"
        
        sql = "SELECT * FROM add_sukien"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        with My_Connection() as db_connection:
            db_connection.cur.execute(sql, params)
            result = db_connection.cur.fetchall()
            if result:
                return result
            return {"message": "No data found"}

    def delete_add_sukien(self, sid: int):
        with My_Connection() as db_connection:
            cur = db_connection.cur
            cur.execute("DELETE FROM add_sukien WHERE id_add = %(sid)s", {"sid": sid})
            if cur.rowcount > 0:
                return JSONResponse(content={"message": "DELETED_SUCCESSFULLY"})
            else:
                raise HTTPException(status_code=404, detail="No record found for the provided sid")

    def patch_add_sukien(self, sid: int, data):
        qry = "UPDATE add_sukien SET "
        for key in data:
            if key != 'id_add':
                qry += f"{key}='{data[key]}',"
        qry = qry[:-1] + f" WHERE id_add = {sid}"
        with My_Connection() as db_connection:
            db_connection.cur.execute(qry)
            if db_connection.cur.rowcount > 0:
                return JSONResponse({"message": "UPDATED_SUCCESSFULLY"}, 200)
            else:
                return JSONResponse({"message": "NOTHING_TO_UPDATE"}, 204)