from sqlmodel import create_engine, SQLModel

from models.users import User

engine = create_engine("sqlite:///./user_center.db", echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)
# init_db()
