from fastapi import Query, Request, APIRouter
from model.add_sukien_model import Add_Sukien_Model

router = APIRouter()
obj = Add_Sukien_Model()


@router.get("/api/add-sukiens")
def get_add_sukiens(request: Request):
    noidung_sukien = request.query_params.get('noidung_sukien', None)
    ten_sukien = request.query_params.get('ten_sukien', None)
    return obj.get_add_sukiens(noidung_sukien, ten_sukien)


@router.delete("/api/add-sukiens/{sid}")
def delete_add_sukiens(sid: int):
    return obj.delete_add_sukien(sid)


@router.patch("/api/add-sukiens/{sid}")
async def edit_add_sukiens(sid: int, request: Request):
    form_data = await request.form()
    return obj.patch_add_sukien(sid, form_data)
