from fastapi import APIRouter, Request
from sqlmodel import select

from models.users import UserRegister, UserLogin, User, UserPublic, CustomerResponse
from api.deps import SessionDep
from core import crud

router = APIRouter()


@router.post('/register', response_model=CustomerResponse)
async def register(session: SessionDep, user_register: UserRegister):
    """ 用户注册
    """
    response = crud.create_user(session, user_register)
    return response


@router.post('/login')
async def login(session: SessionDep, user_login: UserLogin, request: Request):
    """ 用户登录
    """
    response = crud.login(session, user_login, request)
    return response


@router.get('/current', response_model=CustomerResponse)
async def current(request: Request):
    """ 获取当前登录用户
    """
    response = crud.get_active_user(request)
    return response


@router.get('/search', response_model=CustomerResponse)
async def search(session: SessionDep, request: Request):
    response = crud.search_user(session, request)
    return response


@router.post('/logout')
async def login(request: Request):
    """ 用户注销
    """
    response = crud.logout(request)
    return response
