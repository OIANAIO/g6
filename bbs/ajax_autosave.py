from fastapi import APIRouter
from fastapi.params import Depends
from starlette.responses import Response, JSONResponse

from lib.common import *
from common.database import db_session
from common.formclass import AutoSaveForm
from common.models import AutoSave

router = APIRouter()


@router.get("/autosave_list")
async def autosave_list(request: Request, db: db_session):
    """
    자동저장 목록을 보여준다.
    """
    member: Member = request.state.login_member
    if not member:
        raise HTTPException(status_code=403, detail="로그인 후 이용 가능합니다.")

    save_list = db.query(AutoSave).filter(AutoSave.mb_id == member.mb_id).all()
    return save_list


@router.get("/autosave_load/{as_id}")
async def autosave_load(request: Request, as_id: int, db: db_session):
    """
    자동저장 내용을 불러온다.
    """
    member: Member = request.state.login_member
    if not member:
        raise HTTPException(status_code=403, detail="로그인 후 이용 가능합니다.")

    save_data = db.query(AutoSave).filter(AutoSave.mb_id == member.mb_id, AutoSave.as_id == as_id).first()
    return save_data


@router.post("/autosave")
async def autosave(request: Request, db: db_session, form_data: AutoSaveForm = Depends()):
    """
    글 임시저장
    """
    member = request.state.login_member
    if not member:
        raise HTTPException(status_code=403, detail="로그인 후 이용 가능합니다.")
    form_data.mb_id = member.mb_id
    del form_data.as_datetime

    result = db.query(AutoSave).filter(AutoSave.mb_id == form_data.mb_id, AutoSave.as_uid == form_data.as_uid).all()
    if result:
        (db.query(AutoSave).filter(AutoSave.mb_id == form_data.mb_id, AutoSave.as_uid == form_data.as_uid)
         .update(form_data.__dict__))
    else:
        db.add(AutoSave(**form_data.__dict__))

    db.commit()

    count = db.query(AutoSave).filter(AutoSave.mb_id == member.mb_id).count()
    response_data = {
        "count": count,
    }
    return JSONResponse(status_code=201, content=response_data)


@router.delete("/autosave/{as_id}")
async def autosave(request: Request, as_id: int, db: db_session):
    """
    임시저장글 삭제
    """
    member = request.state.login_member
    if not member:
        raise HTTPException(status_code=403, detail="로그인 후 이용 가능합니다.")

    db.query(AutoSave).filter(AutoSave.mb_id == 'ooc', AutoSave.as_id == as_id).delete()
    db.commit()

    return Response(status_code=204, content="삭제되었습니다.")
