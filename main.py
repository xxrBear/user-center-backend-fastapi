import uvicorn
from fastapi import FastAPI
from starlette.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware

from api.main import api_router
from core.exceptions import CustomException

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
app.include_router(api_router)


@app.exception_handler(CustomException)
async def custom_exception_handler(request, exc: CustomException):
    return JSONResponse(status_code=422, content={'description': str(exc.description), 'code': exc.code})


if __name__ == '__main__':
    uvicorn.run(app, port=8080)
