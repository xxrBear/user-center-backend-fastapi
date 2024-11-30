from fastapi import APIRouter, Request
from sqlmodel import select

from models.users import UserRegister, UserLogin, User, UserPublic
from api.deps import SessionDep

router = APIRouter()


@router.post('/register', response_model=UserPublic)
async def register(session: SessionDep, user_register: UserRegister):
    """ 用户注册
    :param session: 依赖
    :param user_register: 模型
    :return: user_id 用户ID
    """
    db_obj = UserRegister.model_validate(user_register)
    user_obj = User(**db_obj.model_dump())
    session.add(user_obj)
    session.commit()
    session.refresh(user_obj)
    json_data = {'code': 0, 'message': 'message', 'description': 'description', 'data': user_obj.id}
    return UserPublic(**json_data)


@router.post('/login')
async def login(session: SessionDep, user_login: UserLogin, request: Request):
    """
    :param session:
    :param user_login:
    :param request:
    :return:
    """
    user_obj = User.model_validate(user_login)
    user_obj = session.exec(select(User).where(User.userAccount == user_obj.userAccount)).first()
    if user_obj:
        request.session.setdefault('userLoginState', user_obj.id)
        return {
            'code': 0,
            'data': user_obj.id,
            'message': 'message',
            'description': 'description',
        }


@router.get('/current')
async def current(session: SessionDep, request: Request):
    """
    :param session:
    :param request:
    :return:
    """
    user_id = request.session.get('userLoginState')
    user_obj = session.exec(select(User).where(User.id == user_id)).one()

    return {
        'code': 0,
        'data': user_obj,
        'message': 'message',
        'description': 'description',
    }


@router.get('/search')
async def search(session: SessionDep, request: Request):
    user_obj = session.exec(select(User)).all()

    return {
        'code': 0,
        'data': user_obj,
        'message': 'message',
        'description': 'description',
    }
