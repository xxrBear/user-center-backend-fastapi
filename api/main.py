from fastapi import APIRouter

from api.routes import users

api_router = APIRouter()
api_router.include_router(users.router, prefix="/api/user", tags=["users"])
