import uvicorn
from fastapi import FastAPI

from starlette.middleware.sessions import SessionMiddleware
from api.main import api_router

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run(app, port=8080)
