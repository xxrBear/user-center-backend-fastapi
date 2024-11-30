from typing import Optional
from datetime import datetime

from pydantic import field_validator
from sqlmodel import SQLModel, Field


class UserBase(SQLModel):  # 使用 table=True 将其注册为数据库表
    id: Optional[int] = Field(default=None, primary_key=True, index=True, description="用户ID")
    username: Optional[str] = Field(default=None, max_length=256, description="用户昵称")
    userAccount: Optional[str] = Field(default=None, max_length=256, description="账号", unique=True)
    avatarUrl: Optional[str] = Field(default=None, max_length=1024, description="用户头像")
    gender: Optional[int] = Field(default=None, description="性别")
    userPassword: str = Field(max_length=512, description="密码")  # 不允许为空
    phone: Optional[str] = Field(default=None, max_length=128, description="电话")
    email: Optional[str] = Field(default=None, max_length=512, description="邮箱")
    userStatus: int = Field(default=0, description="状态 0 - 正常")
    createTime: Optional[datetime] = Field(default_factory=datetime.now, description="创建时间")
    updateTime: Optional[datetime] = Field(default_factory=datetime.now, description="更新时间")
    isDelete: int = Field(default=0, description="是否删除")  # 使用 int 表示布尔值
    userRole: int = Field(default=0, description="用户角色 0 - 普通用户 1 - 管理员")
    planetCode: Optional[str] = Field(default=None, max_length=512, description="星球编号")


class UserRegister(SQLModel):
    userAccount: Optional[str] = Field(min_length=4, max_length=255, nullable=False)
    userPassword: Optional[str] = Field(min_length=8, max_length=128, nullable=False)
    checkPassword: Optional[str] = Field(min_length=8, max_length=128, nullable=False)

    @field_validator("checkPassword")
    def passwords_match(cls, checkPassword, info):
        # 从 ValidationInfo 中获取 userPassword 的值
        userPassword = info.data.get("userPassword")
        if userPassword != checkPassword:
            raise ValueError("两次输入的密码不一致")
        return checkPassword


class UserLogin(SQLModel):
    userAccount: Optional[str] = Field(min_length=4, max_length=255, nullable=False)
    userPassword: Optional[str] = Field(min_length=8, max_length=128, nullable=False)


class User(UserBase, table=True):
    pass


class UserPublic(SQLModel):
    code: int = Field(default=0, description="响应状态码")
    data: int | None = None
    message: str | None = None
    description: str | None = None


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int