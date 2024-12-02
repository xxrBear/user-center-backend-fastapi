import re

from fastapi import Request
from sqlmodel import Session, select
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from core import security, status_code
from core.exceptions import CustomException
from models.users import UserRegister, User, UserPublic, UserLogin, CustomerResponse


def create_user(session: Session, user_register: UserRegister) -> JSONResponse:
    # md5 加密密码
    hashed_password = security.encrypt_with_md5(user_register.userPassword)

    # 判断用户名是否有特殊字符
    pattern = r'[^a-zA-Z0-9_.-]'
    if re.search(pattern, user_register.userAccount):
        raise CustomException(status_code.INVALID_ACCOUNT, '不合法的用户名！')

    statement = select(User).where(User.userAccount == user_register.userAccount)
    username = session.exec(statement).first()
    if username:
        raise CustomException(status_code.USER_EXISTS, '用户名已存在！')

    statement = select(User).where(User.planetCode == user_register.planetCode)
    username = session.exec(statement).first()
    if username:
        raise CustomException(status_code.PLANT_CODE_EXISTS, '星球编号已存在！')

    # 创建一个 User 对象
    db_user = User.model_validate(user_register, update={"userPassword": hashed_password})

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    json_data = {'code': 0, 'message': 'ok', 'description': '创建用户成功！', 'data': db_user}
    return CustomerResponse(**json_data)


def login(session: Session, user_login: UserLogin, request: Request) -> CustomerResponse:
    hashed_password = security.encrypt_with_md5(user_login.userPassword)

    statement = select(User).where(User.userAccount == user_login.userAccount, User.userPassword == hashed_password)
    user_obj = session.exec(statement).first()
    if not user_obj:
        raise CustomException(status_code.LOGIN_ERROR, '用户名或密码错误！')

    user_public = UserPublic(**user_obj.model_dump())
    request.session['userLoginState'] = jsonable_encoder(user_public)
    json_data = {'code': 0, 'message': 'ok', 'description': '登录成功！', 'data': jsonable_encoder(user_public)}

    return CustomerResponse(**json_data)


def logout(request: Request) -> CustomerResponse:
    request.session.clear()
    json_data = {'code': 0, 'message': 'ok', 'description': '注销成功！', 'data': None}
    return CustomerResponse(**json_data)


def get_active_user(request: Request) -> CustomerResponse:
    user_obj = request.session.get('userLoginState')

    if not user_obj:
        raise CustomException(status_code.NOT_LOGIN, '用户未登录！')

    return CustomerResponse(**{
        'code': 0,
        'data': user_obj,
        'message': 'ok',
        'description': '获取登录用户信息！',
    })


def search_user(session: Session, request: Request) -> CustomerResponse:
    has_rule = request.session.get('userLoginState').get('userRole')
    if not has_rule:
        raise CustomException(status_code.NOT_RULE_ERROR, '非管理员用户！')
    user_obj = session.exec(select(User)).all()
    return CustomerResponse(**{
        'code': 0,
        'data': user_obj,
        'message': 'ok',
        'description': '查询用户成功！',
    })
