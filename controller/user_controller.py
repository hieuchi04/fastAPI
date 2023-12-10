from fastapi import Query, Request, APIRouter
from model.user_model import UserModel, User

router = APIRouter()
obj = UserModel()


@router.get('/')
def hello_api():
    return "im hieule in the api !"


@router.get('/api/users')
def all_users(request: Request):
    email = request.query_params.get('email', None)
    ip_register = request.query_params.get('ip_register', None)
    return obj.get_users(email, ip_register)


@router.get('/api/users/search_by_comment')
def get_users_by_comment(request: Request):
    noi_dung_Comment = request.query_params.get('noi_dung', None)
    return obj.get_users_by_comment(noi_dung_Comment)


@router.post("/api/users")
def add_user(data: User):
    return obj.add_user_model(data)


@router.delete("/api/users/{uid}")
def delete_user(uid: int):
    return obj.delete_user_model(uid)


@router.put("/api/users/{uid}")
async def update_user(request: Request, uid: int):
    form_data = await request.form()
    return obj.update_user_model(form_data, uid)


@router.patch("/api/users/{uid}")
async def patch_user(uid: int, request: Request):
    form_data = await request.form()
    return obj.patch_user_model(form_data, uid)
