from pydantic import BaseModel
from configs.mysql_config import My_Connection
from fastapi.responses import JSONResponse


class Saved_sukien(BaseModel):
    id_saved: str
    link_nam_goc: str
    link_nu_goc: str
    link_nam_chua_swap: str
    link_nu_chua_swap: str
    link_da_swap: str
    thoigian_swap: str
    ten_su_kien: str
    noidung_su_kien: str
    id_toan_bo_su_kien: str
    so_thu_tu_su_kien: int
    thoigian_sukien: str
    device_them_su_kien: str
    ip_them_su_kien: str
    id_user: int
    tomLuocText: str
    ten_nam: str
    ten_nu: str
    id_template: int
    phantram_loading: int


class Saved_Sukien_Model:
    def get_saved_sukiens(self):
        with My_Connection() as db_connection:
            db_connection.cur.execute("select * from saved_sukien")
            result = db_connection.cur.fetchall()
            return result

    def delete_saved_sukien(self, sid: int):
        with My_Connection() as db_connection:
            db_connection.cur.execute("DELETE FROM saved_sukien WHERE id_saved = %(sid)s", {"sid": sid})
            if db_connection.cur.rowcount > 0:
                return {"message": "DELETED_SUCCESSFULLY"}
            return {"message": "CONTACT_DEVELOPER"}

    def patch_saved_sukien(self, sid: int, data):
        qry = "UPDATE saved_sukien SET "
        for key in data:
            if key != 'id':
                qry += f"{key}='{data[key]}',"
        qry = qry[:-1] + f" WHERE id_saved = {sid}"
        with My_Connection() as db_connection:
            db_connection.cur.execute(qry)
            if db_connection.cur.rowcount > 0:
                return JSONResponse({"message": "UPDATED_SUCCESSFULLY"}, 200)
            else:
                return JSONResponse({"message": "NOTHING_TO_UPDATE"}, 204)

    def add_sukien(self, data: Saved_sukien):
        sql = "INSERT INTO saved_sukien (id_saved, link_nam_goc, link_nu_goc, link_nam_chua_swap, link_nu_chua_swap, link_da_swap, thoigian_swap, ten_su_kien, noidung_su_kien, id_toan_bo_su_kien, so_thu_tu_su_kien, thoigian_sukien, device_them_su_kien, ip_them_su_kien, id_user, tomLuocText, ten_nam, ten_nu, count_comment, count_view, id_template, phantram_loading) " \
              "VALUES (%(id_saved)s, %(link_nam_goc)s, %(link_nu_goc)s, %(link_nam_chua_swap)s, %(link_nu_chua_swap)s, %(link_da_swap)s, %(thoigian_swap)s, %(ten_su_kien)s, %(noidung_su_kien)s, %(id_toan_bo_su_kien)s, %(so_thu_tu_su_kien)s, %(thoigian_sukien)s, %(device_them_su_kien)s, %(ip_them_su_kien)s, %(id_user)s, %(tomLuocText)s, %(ten_nam)s, %(ten_nu)s, 0, 0, %(id_template)s, %(phantram_loading)s)"

        with My_Connection() as db_connection:
            try:
                db_connection.cur.execute(sql, data.dict())
                if db_connection.cur.rowcount > 0:
                    return JSONResponse(content={"message": "CREATED_SUCCESSFULLY"}, status_code=201)
                else:
                    return JSONResponse(content={"message": "Failed to create sukien"}, status_code=500)
            except Exception as e:
                return JSONResponse(content={e}, status_code=500)

    def saved_sukien_pagination_model(self, pno, limit):
        pno = int(pno)
        limit = int(limit)
        start = (pno * limit) - limit

        # Query to get paginated results with total count
        qry_result = f"SELECT SQL_CALC_FOUND_ROWS * FROM saved_sukien LIMIT {start}, {limit}"
        qry_count = "SELECT FOUND_ROWS() as total_count"

        with My_Connection() as db_connection:
            db_connection.cur.execute(qry_result)
            result = db_connection.cur.fetchall()

            db_connection.cur.execute(qry_count)
            total_count = db_connection.cur.fetchone()['total_count']

            if len(result) > 0:
                return JSONResponse({
                    "page": pno,
                    "per_page": limit,
                    "total_records": total_count,
                    "this_page": len(result),
                    "payload": result
                })
            else:
                return JSONResponse({"message": "No Data Found"}, 204)
