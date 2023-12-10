from fastapi import Request, APIRouter
from service.checking_img import checking_img

router = APIRouter()


@router.post("/api/check-img")
async def check_img(request: Request):
    form_data = await request.form()
    return checking_img(form_data.get("link_img"))
