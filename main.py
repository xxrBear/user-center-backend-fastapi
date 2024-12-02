import uvicorn
from fastapi import FastAPI
from starlette.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware

from api.main import api_router
from core.exceptions import CustomException
from core.init_db import init_db_and_superuser

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
app.include_router(api_router)
# 允许所有来源
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,  # 允许携带 cookies
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)


# FastAPI 启动时初始化数据库
@app.on_event("startup")
def startup():
    init_db_and_superuser()


@app.exception_handler(CustomException)
async def custom_exception_handler(request, exc: CustomException):
    return JSONResponse(status_code=422, content={'description': str(exc.description), 'code': exc.code})


if __name__ == '__main__':
    uvicorn.run(app, port=8080)
