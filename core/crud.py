from fastapi import Request
from sqlmodel import Session, select
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from models.users import UserRegister, User, UserPublic, UserLogin, CustomerResponse
from core import security


def create_user(session: Session, user_register: UserRegister) -> CustomerResponse:
    # md5 加密密码
    hashed_password = security.encrypt_with_md5(user_register.userPassword)
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
        raise ValueError('用户名或密码错误！')

    user_public = UserPublic(**user_obj.model_dump())
    request.session.setdefault('userLoginState', jsonable_encoder(user_public))
    json_data = {'code': 0, 'message': 'ok', 'description': '登录成功！', 'data': user_public}

    return CustomerResponse(**json_data)


def logout(request: Request) -> CustomerResponse:
    request.session.setdefault('userLoginState', '')
    json_data = {'code': 0, 'message': 'ok', 'description': '注销成功！', 'data': None}
    return CustomerResponse(**json_data)


def get_active_user(request: Request) -> CustomerResponse:
    user_obj = request.session.get('userLoginState')

    return CustomerResponse(**{
        'code': 0,
        'data': user_obj,
        'message': 'ok',
        'description': '获取登录用户信息！',
    })


def search_user(session: Session, request: Request, username: str | None = None) -> CustomerResponse:
    if username:
        pass
    user_obj = session.exec(select(User)).all()

    return CustomerResponse(**{
        'code': 0,
        'data': user_obj,
        'message': 'ok',
        'description': '查询用户成功！',
    })
