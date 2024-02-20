from fastapi import APIRouter, Query
from starlette.requests import Request

from core.template import theme_asset, UserTemplates
from lib.pbkdf2 import create_hash
from .. import plugin_config
from ..plugin_config import module_name

from sqlalchemy import or_, select, update, delete, func, DateTime
from core.database import db_session
from core.models import Member
from pydantic import BaseModel
from datetime import datetime


router = APIRouter()

templates = UserTemplates()
templates.env.globals["theme_asset"] = theme_asset


@router.get("/users")
# def show(request: Request):
#     return {"message": "GET users"}
async def read_users(
    request: Request,
    db: db_session,
    page: int = Query(default=1, ge=1)):
    """
    사용자 요청을 처리하는 경로.
    - page: 쿼리 파라미터로 받은 페이지 번호 (기본값: 1, 1 이상이어야 함)
    """
    # 사용자 데이터를 10개씩 가져옵니다.
    query = select(Member).order_by(Member.mb_no).limit(10).offset((page - 1) * 10)
    # 관리자 데이터가 있어야 되는데 어디갔지?
    # query = select(Member).where(or_(Member.mb_id == "admin", Member.mb_id == "test"))
    members = db.scalars(query).all()
    # 여기에 페이지 번호에 따라 사용자 데이터를 가져오는 로직을 구현합니다.
    # 예를 들어, 페이지 번호에 따라 데이터베이스에서 사용자 정보를 조회할 수 있습니다.
    return {"page": page, "data": members}


class UserCreate(BaseModel):
    mb_id: str
    mb_password: str
    mb_name: str
    mb_nick: str
    mb_ip: str
    mb_datetime: datetime


@router.post("/users")
# def show(request: Request):
#     return templates.TemplateResponse(
#         f"{plugin_config.TEMPLATE_PATH}/user_demo.html",
#         {
#             "request": request,
#             "title": f"Hello plugin Template!",
#             "content": f"Hello {module_name}!",
#         })
async def add_user(
    user: UserCreate, 
    db: db_session,):

    user.mb_password = create_hash(user.mb_password)
    db_user = Member(
        mb_id=user.mb_id,
        mb_password=user.mb_password,
        mb_name=user.mb_name,
        mb_nick=user.mb_nick,
        mb_ip=user.mb_ip,
        mb_datetime=user.mb_datetime
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user