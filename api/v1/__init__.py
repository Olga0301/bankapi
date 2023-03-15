from fastapi import APIRouter
from .post import post_router

v1_router = APIRouter(prefix='/v1')
v1_router.include_router(router=post_router)
