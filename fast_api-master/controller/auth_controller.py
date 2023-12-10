from fastapi import Request, APIRouter, Depends
from model.auth_model import Auth_Model
from jwt_auth.auth_bearer import JWTBearer

router = APIRouter()
obj = Auth_Model()


@router.post("/api/users/change-password/{uid}", dependencies=[Depends(JWTBearer())])
async def change_user_password(uid: int, request: Request):
    form_data = await request.form()
    return obj.change_user_password(form_data, uid)


@router.post("/api/users/login")
async def login_user(request: Request):
    form_data = await request.form()
    return obj.login_user(form_data)
