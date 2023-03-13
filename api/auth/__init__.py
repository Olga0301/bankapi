from fastapi import APIRouter

from .auth import router


auth_router = APIRouter(prefix='/auth')
auth_router.include_router(router=router)
