import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, SQLModel
from sqlalchemy.orm import sessionmaker

from main import app  # 导入 FastAPI 应用实例
from models.users import UserRegister, User

from api.deps import get_db

# 创建 TestClient 实例
client = TestClient(app)

# 设置一个内存中的 SQLite 数据库来进行测试
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建所有表
SQLModel.metadata.create_all(bind=engine)


# 依赖注入的替换函数
def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 使用 pytest fixture 来初始化测试客户端
@pytest.fixture()
def new_client():
    # 替换数据库依赖
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    # 清理数据库
    db = SessionLocal()
    db.query(UserRegister).delete()
    db.commit()


def test_create_user():
    # 构造请求体的数据
    item_data = {
        "userAccount": "adminxxx",
        "userPassword": "admin123",
        "checkPassword": "admin123",
        "planetCode": "10086"
    }

    # 发送 POST 请求
    response = client.post("/api/user/register", json=item_data)

    # 断言响应状态码
    assert response.status_code == 200

    # 断言返回的 JSON 数据
    assert response.json() == {"name": "Sample Item", "price": 10.5}
