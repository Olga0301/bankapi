from fastapi import FastAPI

from api.auth import auth_router
from api import api_router

app = FastAPI()
app.include_router(router=auth_router)
app.include_router(router=api_router)
