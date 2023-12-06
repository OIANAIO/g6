from fastapi import APIRouter, Depends, File, Form, Path, Query, Request, UploadFile
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from common.formclass import ContentData, ContentForm
from common.database import get_db
from lib.plugin.service import get_admin_plugin_menus, get_all_plugin_module_names
from common.models import Content
from lib.common import *
from dataclasses import asdict

router = APIRouter()
templates = AdminTemplates()
# 파이썬 함수 및 변수를 jinja2 에서 사용할 수 있도록 등록
templates.env.globals["now"] = now
templates.env.globals["get_admin_plugin_menus"] = get_admin_plugin_menus
templates.env.globals["get_all_plugin_module_names"] = get_all_plugin_module_names
templates.env.globals["get_skin_select"] = get_skin_select
templates.env.globals["get_admin_menus"] = get_admin_menus
templates.env.globals["get_head_tail_img"] = get_head_tail_img

MENU_KEY = "300600"
IMAGE_DIRECTORY = "data/content/"


@router.get("/content_list")
def content_list(request: Request, db: Session = Depends(get_db)):
    """
    내용관리 목록
    """
    request.session["menu_key"] = MENU_KEY

    contents = db.query(Content).all()
    return templates.TemplateResponse(
        "content_list.html", {"request": request, "contents": contents}
    )


@router.get("/content_form")
def content_form_add(request: Request, db: Session = Depends(get_db)):
    """
    내용추가 폼
    """
    return templates.TemplateResponse(
        "content_form.html", {"request": request, "content": None}
    )


@router.get("/content_form/{co_id}")
def content_form_edit(co_id: str, request: Request, db: Session = Depends(get_db)):
    """
    내용 수정 폼
    """
    content = db.query(Content).filter(Content.co_id == co_id).first()
    if not content:
        raise AlertException(status_code=404, detail=f"{co_id} : 내용 아이디가 존재하지 않습니다.")

    return templates.TemplateResponse(
        "content_form.html",
        {"request": request, "content": content},
    )


@router.post("/content_form_update")
def content_form_update(request: Request,
                        db: Session = Depends(get_db),
                        action: str = Form(...),
                        token: str = Form(...),
                        co_id: str = Form(...),
                        # form_data: ContentForm = Depends(),
                        form_data: ContentForm = Depends()):
    """내용등록 및 수정 처리

    - 내용 등록 및 수정 데이터 저장
    - 이미지파일 저장

    Args:
        request (Request): 
        db (Session, optional): 
        token (str): 입력/수정/삭제 변조 방지 토큰.
        co_id (str): 내용 ID.
        form_data (ContentDataclass): 입력/수정 Form Data.
        co_himg (UploadFile, optional): 상단 이미지 첨부파일. Defaults to File(...).
        co_timg (UploadFile, optional): 하단 이미지 첨부파일. Defaults to File(...).
        co_himg_del (int, optional): 상단 이미지 삭제체크. Defaults to None.
        co_timg_del (int, optional): 하단 이미지 삭제체크. Defaults to None.

    Raises:
        AlertException: 유효한 토큰인지 체크
        AlertException: 아이디 중복체크.
        AlertException: 아이디 존재여부 체크.

    Returns:
        RedirectResponse: 내용 등록/수정 후 상세 폼으로 이동
    """
    if not check_token(request, token):
        raise AlertException("토큰이 유효하지 않습니다", 403)
    
    # Form Data => Content Data
    content_data = create_dataclass_instance(form_data, ContentData)

    if action == "w":
        # ID 중복 검사
        exists_content = db.query(Content).filter(Content.co_id == co_id).first()
        if exists_content:
            raise AlertException(status_code=400, detail=f"{co_id} : 내용 아이디가 이미 존재합니다.")
        
        # 내용 등록
        content = Content(co_id=co_id, **content_data.__dict__)
        db.add(content)
        db.commit()

    elif action == "u":
        content = db.get(Content, co_id)
        if not content:
            raise AlertException(status_code=404, detail=f"{co_id} : 내용 아이디가 존재하지 않습니다.")

        # 데이터 수정 후 commit
        for field, value in content_data.__dict__.items():
            setattr(content, field, value)
        db.commit()

    # 이미지 경로체크 및 생성
    make_directory(IMAGE_DIRECTORY)
    # 이미지 삭제
    delete_image(IMAGE_DIRECTORY, f"{co_id}_h", form_data.co_himg_del)
    delete_image(IMAGE_DIRECTORY, f"{co_id}_t", form_data.co_timg_del)
    # 이미지 저장
    save_image(IMAGE_DIRECTORY, f"{co_id}_h", form_data.co_himg)
    save_image(IMAGE_DIRECTORY, f"{co_id}_t", form_data.co_timg)

    
    return RedirectResponse(url=request.url_for('content_form_edit', co_id=co_id), status_code=302)


@router.get("/content_delete/{co_id}")
def content_delete(request: Request, 
                   db: Session = Depends(get_db),
                   token: str = Query(...),
                   co_id: str = Path(...)):
    """
    내용 삭제
    """
    if not check_token(request, token):
        raise AlertException("토큰이 유효하지 않습니다", 403)
    
    content = db.query(Content).filter(Content.co_id == co_id).first()
    if not content:
        raise AlertException(status_code=404, detail=f"{co_id}: 내용 아이디가 존재하지 않습니다.")

    # 이미지 삭제
    delete_image(IMAGE_DIRECTORY, f"{co_id}_h")
    delete_image(IMAGE_DIRECTORY, f"{co_id}_t")
    # 내용 삭제
    db.delete(content)
    db.commit()

    return RedirectResponse(url=request.url_for('content_list'), status_code=302)


def create_dataclass_instance(source_instance: object, target_dataclass: object):
    """Dataclass 인스턴스 생성
    - source_instance 에서 target_dataclass 에 정의된 필드만 추출하여 인스턴스 생성
    - 주로 폼 데이터를 데이터 클래스 인스턴스로 변환할 때 사용

    Args:
        source_instance (object): 폼 데이터
        target_dataclass (object): 데이터 클래스 인스턴스

    Returns:
        object: 데이터 클래스 인스턴스
    """
    source_dict = asdict(source_instance)
    valid_fields = {k: v for k, v in source_dict.items() if k in target_dataclass.__dataclass_fields__}

    return target_dataclass(**valid_fields)