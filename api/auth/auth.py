from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from core.models import User
from core.schemas import UserInfo, RegisterForm, LoginForm


router = APIRouter()


@router.post(
    '/register',
    response_model=UserInfo,
    response_model_exclude={'password', 'hashed_password', 'pk'},
    status_code=status.HTTP_201_CREATED
)
async def register_user(register_form: RegisterForm):
    user_info = UserInfo(**register_form.dict())
    user = User(**user_info.dict(exclude={'pk', 'password'}))
    try:
        await user.save()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='почта или имя пользователя не уникальны')
    else:
        return user_info


@router.post(
    '/login',
    response_model=UserInfo,
    response_model_exclude={'password', 'hashed_password', 'pk'}
)
async def login(login_form: LoginForm):
    user = await User.select(User.email == login_form.email)
    if user:
        user = user[0]
        try:
            user_info = UserInfo(**login_form.dict() | {
                'hashed_password': user.hashed_password,
                'username': user.username
                }
            )
        except ValidationError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='не верный пароль')
        else:
            return user_info
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='пользователь не найден')