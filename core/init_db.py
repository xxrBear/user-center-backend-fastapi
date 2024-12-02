from sqlalchemy.engine import reflection
from sqlmodel import create_engine, SQLModel, Session, select

from models.users import User
from core.security import encrypt_with_md5

engine = create_engine("sqlite:///./user_center.db", echo=True)


# 初始化数据库表
def init_db_and_superuser():
    # 检查是否已经有表，避免重复创建
    inspector = reflection.Inspector.from_engine(engine)
    if 'user' not in inspector.get_table_names():  # 如果没有名为 'user' 的表
        SQLModel.metadata.create_all(bind=engine)

    # 创建管理员账号
    with Session(engine) as session:
        statement = select(User).where(User.userAccount == 'admin')
        super_user = session.exec(statement).first()
        if not super_user:
            user_info = {
                'userAccount': 'admin',
                'userPassword': encrypt_with_md5('admin123'),
                'avatarUrl': 'https://cdn.jsdelivr.net/gh/xxrBear/image//Hugo/202411291606062.png',
                'userRole': 1,
            }

            super_user = User(**user_info)
            session.add(super_user)
            session.commit()
            session.refresh(super_user)
